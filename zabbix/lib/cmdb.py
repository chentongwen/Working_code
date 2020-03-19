#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
'''
@AUTHOR: Mr.CTW
@DATE: 2020/03/02 周一
@Contact: 18639888259@168.com
'''
# here put the import lib
import json,os,requests
import conf.settings

class CMDB(object):
    #获取cmdb token函数
    def token(self):
        rq = requests.post(url=conf.settings.cmdb_token,params=conf.settings.cmdb_login)
        result = json.loads(rq.text)
        return result

    #获取所有应用的名称函数
    def app_name(self):
        rq = requests.get(conf.settings.cmdb_app_name)
        result = json.loads(rq.text)
        return result
    
    #获取指定应用名信息
    def specific_app(self,token,app_name):
        header = {'X-Token':token}
        rq = requests.get(conf.settings.cmdb_app_specific+app_name,headers=header)
        result=json.loads(rq.text)
        return result
    
    #获取所有服务器信息
    def host_all(self,token):
        header = {'X-Token':token}
        rq = requests.get(conf.settings.cmdb_server,headers=header)
        result = json.loads(rq.text)
        return result

    #获取指定ip简略信息
    def host_ip(self,ip):
        rq = requests.get(conf.settings.cmdb_specific_ip+ip)
        result = json.loads(rq.text)
        return result
    
    #获取指定服务器ip的主机信息
    def server_ip(self,token,ip):
        header = {'X-Token':token}
        rq = requests.get(conf.settings.cmdb_server_ip+ip,headers=header)
        result = json.loads(rq.text)
        return result

    