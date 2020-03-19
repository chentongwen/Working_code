#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
'''
@AUTHOR: Mr.CTW
@DATE: 2020/03/02 周一
@Contact: 18639888259@168.com
'''
# here put the import lib
import conf.settings
import json,requests

#获取指定um在sso统一认证平台的详细信息
class SSO(object):
    #通过指定um获取指定人详细信息。
    def sso_um(self,um):
        rq=requests.get(conf.settings.sso_um+um)
        result=json.loads(rq.text)
        return result