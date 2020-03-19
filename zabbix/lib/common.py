#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
'''
@AUTHOR: Mr.CTW
@DATE: 2020/03/02 周一
@Contact: 18639888259@168.com
'''
# here put the import lib
import conf.settings
import logging
import logging.config
import json

'''
公共组件部分
'''
def get_logger(name):
    logging.config.dictConfig(conf.settings.LOGGING_DIC)  #导入setting文件配置的logging配置
    logger = logging.getLogger(name) #生成一个log实例
    return logger
    