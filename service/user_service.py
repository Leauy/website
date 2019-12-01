#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
@author: leauy
'''
import traceback
from blog.const.error_code import ErrorConstant
from blog.utils.dbtools import SchedDB
from blog.utils.logger import getLogger

class UserService(object):
    def __init__(self):
        self.logger = getLogger()

    # 获取用户列表
    def get_user_list(self):
        conn = None
        try:
            conn = SchedDB.get_conn()
            ret = conn.select("select id, username, nickname, update_time, is_enable FROM USER")
            return True, ret
        except:
            self.logger.error(traceback.format_exc())
            return False, ErrorConstant.DATABASE_OPERATE_ERROR
        finally:
            conn.close()

    # 获取用户信息
    def get_user_info(self, user_id):
        if not user_id:
            return False, ErrorConstant.USER_ID_IS_NULL
        conn = None
        try:
            conn = SchedDB.get_conn()
            tmp = conn.select("SELECT id, username, nickname, update_time, is_enable FROM USER WHERE id = %s", (user_id))
            if tmp and tmp[0]:
                return True, tmp[0]
            else:
                return False, ErrorConstant.USER_IS_NOT_EXIST
        except:
            self.logger.error(traceback.format_exc())
        finally:
            conn.close()

    # 创建用户
    def create_user(self, user):
        if not user:
            return False, ErrorConstant.USER_IS_NULL
        username = user.get('username')
        password = user.get('password')
        nickname = user.get('nickname')
        if not username:
            return False, ErrorConstant.USERNAME_IS_NULL
        if not password:
            return False, ErrorConstant.PASSWORD_IS_NULL
        self.logger.info("create user params,username(%s), nickname(%s)" % (username, nickname))
        conn = None
        try:
            conn = SchedDB.get_conn()
            sql = "INSERT INTO user (username, nickname, password, update_time, is_enable)" \
                  " VALUE (%s, %s, %s, NOW(), 1)"
            conn.execute(sql, (username, nickname, password))
            conn.commit()

            new_user_ret = conn.select("SELECT MAX(id) as new_user_id FROM USER")
            if new_user_ret and new_user_ret[0]:
                return True, new_user_ret[0]["new_user_id"]
        except:
            self.logger.error(ErrorConstant.DATABASE_OPERATE_ERROR.errMsg)
            return False, ErrorConstant.DATABASE_OPERATE_ERROR
        finally:
            conn.close()

    # 删除用户
    def delete_user(self, user_id):
        conn = None
        try:
            conn = SchedDB.get_conn()
            conn.execute("delete from user where id = %s", (user_id))
            conn.commit()
            self.logger.warning("delete user(%s)" % user_id)
            return True, ErrorConstant.SUCCESS
        except:
            self.logger.error(traceback.format_exc())
            return False, ErrorConstant.DATABASE_OPERATE_ERROR
        finally:
            conn.close()

    # 更新用户
    def update_user(self, user):
        conn = None
        try:
            conn = SchedDB.get_conn()
            sql = "update user set "
            params = []
            nickname = user.get('nickname')
            is_enable = user.get('is_enable')
            user_id = user.get('id')
            if user_id == None:
                return False, ErrorConstant.USER_IS_NOT_EXIST

            if nickname == None and is_enable == None:
                return False, ErrorConstant.NICK_NAME_AND_IS_ENABLE_NULL

            if nickname:
                sql += ' nickname = %s,'
                params.append(nickname)
            if is_enable != None:
                sql += ' is_enable = %s,'
                params.append(is_enable)

            sql += ' update_time=NOW() where id = %s'
            params.append(user_id)
            conn.execute(sql, tuple(params))
            conn.commit()
            return True, ErrorConstant.SUCCESS
        except:
            self.logger.error(traceback.format_exc())
            return False, ErrorConstant.DATABASE_OPERATE_ERROR
        finally:
            conn.close()

    # 用户登录
    def login(self, user):
        pass

    # 用户登出
    def logout(self, user):
        pass

if __name__ == '__main__':
    user_service = UserService()
    # new_user = {
    #     "username": u"jidf3233dfji",
    #     "nickname": u"刘洋sdaf答复",
    #     "password": u"nsfocus123",
    # }
    # flag, msg = user_service.create_user(new_user)
    # print(flag, msg)
    # if flag:
    #     new_user_id = msg
    #     print(user_service.get_user_info(new_user_id))
    #     print(user_service.delete_user(new_user_id))
    #     tmp_flag, ss = user_service.get_user_info(new_user_id)
    #     if tmp_flag == False and ss == ErrorConstant.USER_IS_NOT_EXIST:
    #         print("user is not exist has been deleted")
    # print(user_service.get_user_list())
    print(user_service.get_user_info(5))
    modify_user = {
        'id': 5,
        'nickname': 'sbsbsb',
        'is_enable': False
    }
    user_service.update_user(modify_user)
    print(user_service.get_user_info(5))


