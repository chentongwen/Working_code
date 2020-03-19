#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
'''
@AUTHOR: Mr.CTW
@DATE: 2020/03/03 周二
@Contact: 18639888259@168.com
脚本思路：
1、获取cmdb/zabbix上所有的ip并在各自上都具有唯一性（集合）
2、cmdb与zabbix比较取差集（cmdb上在运行状态的ip，并在zabbix上没有的ip）
3、获取添加主机所需的信息
4、在zabbix上添加主机
'''
# here put the import lib
'''
自动添加主机的脚本
'''
import json
import lib.common,lib.cmdb,lib.zabbix,lib.sso
import conf.settings

#log 实例
logger=lib.common.get_logger(__name__)
logger.info('{0}{1}{2}'.format('*'*30,'运行add_host.py脚本','*'*30))
#cmdb 实例
cmdb = lib.cmdb.CMDB()

#zabbix 实例
zab = lib.zabbix.ZABBIX()

#sso平台实例
sso = lib.sso.SSO()

#获取cmdb token
try:
    cmdb_token=cmdb.token()['token']
except BaseException as e:
    logger.error('获取cmdb token 失败')
    logger.error(e)
else:
    logger.info('获取cmdb token成功')


#获取zabbix token
try:
    zab_token = zab.token()['result']
except BaseException as e:
    logger.error('获取zabbix token失败')
    logger.error(e)
else:
    logger.info('获取zabbix token 成功')

#获取zabbix上所有主机
logger.info('获取zabbix上所有主机')
zab_all_host = zab.host_all(zab_token)
with open(conf.settings.ZAB_ALL_HOST,'w+',encoding='utf-8')as f1:
    f1.write(json.dumps(zab_all_host,indent=2,ensure_ascii=False))
zab_all_ip=set() #提取ip
for single_zab_host in zab_all_host['result']:
    zab_ip = single_zab_host['interfaces'][0]['ip']
    zab_all_ip.add(zab_ip)


#获取cmdb上所有的主机
logger.info('获取cmdb上所有的主机')
cmdb_all_host = cmdb.host_all(cmdb_token)
with open(conf.settings.CMDB_ALL_HOST,'w+',encoding='utf-8')as f2:
    f2.write(json.dumps(cmdb_all_host,indent=2,ensure_ascii=False))
cmdb_all_ip = set() #提取ip
for single_cmdb_host in cmdb_all_host['data']:
    server_status = single_cmdb_host['server_status']
    cmdb_ip = single_cmdb_host['ip_address']
    if server_status == ['运行中']:
        cmdb_all_ip.add(cmdb_ip)
    else:
        continue

#比较cmdb/zabbix上的ip,获取cmdb上有zabbix上没有的ip
logger.info('cmdb与zabbix对比')
add_ip = cmdb_all_ip.difference(zab_all_ip)
with open (conf.settings.BLACKLIST,'r',encoding='utf-8')as r1:
    blacklist=json.loads(r1.read())
blacklist_ip = set(blacklist['host'])
add_ip = list(add_ip.difference(blacklist_ip))
# add_ip = ['10.191.80.46']
if len(add_ip) == 0:
    logger.info('cmdb上运行状态的主机都存在zabbix中')
else:
    logger.info('cmdb上未在zabbix上存在的主机{0}'.format(add_ip))
    for ip in add_ip:
        ip_data = cmdb.host_ip(ip) #获取主机系统和负责人信息
        # with open(conf.settings.CMDB_IP,'w+',encoding='utf-8')as f3:
        #     f3.write(json.dumps(ip_data,indent=2,ensure_ascii=False))
        owner = ip_data['serverInfo']['owner']
        os = ip_data['serverInfo']['os_name']
        os = (os.split()[0]).lower()
        server_data = cmdb.server_ip(token=cmdb_token,ip=ip) #获取服务器环境信息是dev、sit。。。
        env = server_data['data'][0]['env_name']
        #判断需要添加主机的主机在是生产环境（prd）还是其他环境和系统，决定主机需要连接的模板
        if env == 'prd':
            if os in ['linux', 'ubuntu', 'centos', 'opensuse', 'suse', 'freebsd']:
                tempid = '12491'
            else:
                tempid = '12519'
        else:
            if os in ['linux', 'ubuntu', 'centos', 'opensuse', 'suse', 'freebsd']:
                tempid = '12572'
            else:
                tempid = '12573'
        #主机所在的主机组id
        owner_data = sso.sso_um(owner)
        logger.info(owner_data)
        department = owner_data['user_info']['department'] #主机所在部门
        with open(conf.settings.HOST_GROUP_PATH,'r',encoding='utf-8')as f3:
            hostGroup = json.loads(f3.read())
        if department in hostGroup:
            logger.info('主机所在部门在zabbix上存在主机群组')
            groupid = hostGroup[department]
        else:
            logger.error('主机所在部门在zabbix上未存在主机群组，请知悉！！ 群组：{0} 主机：{1}'.format(department,ip))
            continue
        #主机代理id
        if ip[0:6]  == '10.185':
            proxyid = '12587'
        else:
            proxyid = '10263'
        #主机名称
        host_name = 'vm-{0}-{1}'.format(ip,os)
        host_name = host_name.replace('.','-')
        #添加主机
        add_host = zab.add_host(token=zab_token,ip=ip,host_name=host_name,tempid=tempid,proxyid=proxyid,groupid=groupid)
        logger.info(add_host)
logger.info('{0}{1}{2}'.format('*'*30,'add_host.py脚本执行完毕','*'*30))

