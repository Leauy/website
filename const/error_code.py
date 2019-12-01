#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
@author: leauy
'''

from collections import namedtuple

ErrorMsg = namedtuple('ErrorMsg', ['errCode', 'errMsg'])

class ErrorConstant(object):
    SUCCESS = ErrorMsg(0, 'success')
    USER_IS_NULL = ErrorMsg(1000, 'user is null')
    USERNAME_IS_NULL = ErrorMsg(1001, 'username is null')
    PASSWORD_IS_NULL = ErrorMsg(1002, 'password is null')
    USER_ID_IS_NULL = ErrorMsg(1003, 'user_id is null')
    USER_IS_NOT_EXIST = ErrorMsg(1004, 'user is not exist')
    NICK_NAME_AND_IS_ENABLE_NULL = ErrorMsg(1005, 'nickname and is_enable is null')
    DATABASE_OPERATE_ERROR = ErrorMsg(2000, 'operate database error')


