#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
'''
@AUTHOR: Mr.CTW
@DATE: 2020/03/02 周一
@Contact: 18639888259@168.com
'''
# here put the import lib
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_NAME_PATH = os.path.join(BASE_DIR,'db','app_name.json')
HOST_GROUP_PATH = os.path.join(BASE_DIR,'db','hostGroup.json') #zabbix上主机组编号
CMDB_ALL_HOST = os.path.join(BASE_DIR,'db','cmdb_all_host.json') #cmdb上所有服务器信息
CMDB_IP = os.path.join(BASE_DIR,'db','cmdb_ip.json') #获取指定ip在cmdb上的信息
ZAB_ALL_HOST = os.path.join(BASE_DIR,'db','zab_all_host.json') #zabbix上所有服务器信息
BLACKLIST = os.path.join(BASE_DIR,'db','blacklist.json') #需要略过的ip,temp（黑名单）
LOG_PATH = os.path.join(BASE_DIR,'log','SHT.log')
LOGIN_TIMEOUT = 3 


'''
CMDB
'''
#账户
cmdb_user = "xxxx"
cmdb_password = "xxxxx"
cmdb_login = {'username':cmdb_user,'password':cmdb_password}

#api接口
cmdb_server_ip="xxxx"
cmdb_server = "xxxxx" #获取所有服务器信息
cmdb_specific_ip = "xxxxx"  #获取指定IP信息
cmdb_token = 'xxxx' #获取token
cmdb_app_name = "xxxxx" #获取所有应用名字
cmdb_app_specific = "xxxx" #获取指定应用名字的信息

'''
ZABBIX
'''
#账户
zab_user = 'xxxxx'
zab_password = 'xxxxx'
zab_api = 'xxxxx'
zab_header = {'Content-Type':'application/json'}

'''
SSO
'''
sso_um = 'xxxxxxx'  #获取指定um人员信息


'''
logging配置
'''
# 定义三种日志输出格式
# 标准格式
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'  # 其中name为getlogger指定的名字
# 简单格式
simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
# id简单格式
id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': id_simple_format
        },
        'simple': {
            'format': id_simple_format
        },
    },
    'filters': {},
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        # 打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': LOG_PATH,  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}