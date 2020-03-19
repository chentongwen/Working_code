#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
'''
@AUTHOR: Mr.CTW
@DATE: 2020/03/02 周一
@Contact: 18639888259@168.com
'''
# here put the import lib
import conf.settings
import os,json,requests

class ZABBIX(object):
    #获取token
    def token(self):
        data={
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": conf.settings.zab_user,
                "password": conf.settings.zab_password
            },
            "id": "token"
        }
        rq=requests.post(url=conf.settings.zab_api,headers=conf.settings.zab_header,data=json.dumps(data))
        result=json.loads(rq.text)
        return result   
    
    #获取指定ip信息
    def host_ip(self,token,ip):
        data={
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ['hostid'],
                "filter":{
                    'ip':ip
                },
                "selectParentTemplates":[
                    "templateid",
                    "name"
                ],
            },
            "id": "host.get host ip",
            'auth': token
        }
        rq=requests.post(url=conf.settings.zab_api,headers=conf.settings.zab_header,data=json.dumps(data))
        result=json.loads(rq.text)
        return result

    #链接应用模板
    def service_temp(self,token,hostid,tempid):
        data={
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": {
                "hostid": hostid,
                "templates": tempid
            },
            "id": "host.update service templates",
            "auth": token
        }
        rq=requests.post(url=conf.settings.zab_api,headers=conf.settings.zab_header,data=json.dumps(data))
        result=json.loads(rq.text)
        return result
    
    #获取zabbix上所有主机
    def host_all(self,token):
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "hostid",
                    "host"
                ],
                "selectInterfaces": [
                    "interfaceid",
                    "ip"
                ],
            },
            "id": '获取all server信息',
            "auth": token
        }
        request = requests.post(url=conf.settings.zab_api, headers=conf.settings.zab_header, data=json.dumps(data))
        result = json.loads(request.text)
        return result
    #添加主机
    def add_host(self, token, ip, host_name, tempid, proxyid, groupid):
        data = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": host_name,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": ip,
                        "dns": "",
                        "port": "10050"
                    }
                ],
                "proxy_hostid": proxyid,
                "groups": [
                    {
                        "groupid": groupid
                    }
                ],
                "templates": [
                    {
                        "templateid": tempid
                    }
                ],
            },
            "auth": token,
            "id": "add host ok"
        }
        rq = requests.post(url=conf.settings.zab_api, headers=conf.settings.zab_header, data=json.dumps(data))
        result = json.loads(rq.text)
        return result
