#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
@author: leauy
'''
from blog.service.user_service import UserService
from blog.utils.dbtools import SchedDB
from blog.utils.logger import getLogger
from blog.const.config import INIT_SQL_PATH
from blog.const.error_code import ErrorConstant
import unittest
import traceback
first_new_user_id = None
has_init = False

class TestUserService(unittest.TestCase):
    def setUp(self):
        global has_init
        self.logger = getLogger()
        self.logger.info("start test")
        if not has_init:
            self.logger.info("init database sql")
            conn = None
            try:
                conn = SchedDB.get_conn()
                sql = ""
                with open(INIT_SQL_PATH, 'r') as f:
                    for line in f.readlines():
                        sql += line
                sql = sql.replace('\n', ' ')
                sqls = sql.split(';')
                for l in sqls:
                    if l:
                        conn.execute(l)
                conn.commit()
            except:
                self.logger.error(traceback.format_exc())
            finally:
                conn.close()
            has_init = True
        self.user_service = UserService()

    def tearDown(self):
        self.logger.info("finish test")

    def test_1_create_user(self):
        global first_new_user_id
        self.logger.info("test create_user start")
        new_user_params = {
            "username": "liuyang",
            "nickname": "刘洋",
            "password": "nsfocus"
        }
        flag, new_user_id = self.user_service.create_user(new_user_params)
        first_new_user_id = new_user_id
        self.assertEqual(flag, True)
        self.assertEqual(new_user_id, 1, "新创建的用户id为1")
        user_info_flag, new_user_info = self.user_service.get_user_info(new_user_id)
        self.assertEqual(user_info_flag, True)
        self.assertEqual(new_user_info['username'], new_user_params['username'], "新建的用户名和参数用户名相等")
        self.assertEqual(new_user_info['nickname'], new_user_params['nickname'], '新建的昵称和参数昵称相等')
        self.logger.info("test create_user end")


    def test_2_update_user(self):
        self.logger.info("test update_user start")
        update_user_params1 = {
            "nickname": "张三",
            "id": first_new_user_id
        }
        update_flag, msg = self.user_service.update_user(update_user_params1)
        self.assertEqual(update_flag, True)
        self.assertEqual(msg, ErrorConstant.SUCCESS)
        user_info_flag, new_user_info = self.user_service.get_user_info(first_new_user_id)
        self.assertEqual(user_info_flag, True)
        self.assertEqual(new_user_info['nickname'], update_user_params1['nickname'], '更新的昵称和更新参数昵称相等')

        update_user_params2 = {
            "id": first_new_user_id,
            "nickname": "李四",
            "is_enable": False
        }
        update_flag, msg = self.user_service.update_user(update_user_params2)
        self.assertEqual(update_flag, True)
        self.assertEqual(msg, ErrorConstant.SUCCESS)
        user_info_flag, new_user_info = self.user_service.get_user_info(first_new_user_id)
        self.assertEqual(user_info_flag, True)
        self.assertEqual(new_user_info['nickname'], update_user_params2['nickname'], '更新的昵称和更新参数昵称相等')
        self.assertEqual(new_user_info['is_enable'], update_user_params2['is_enable'], '更新的是否启用和更新参数相等')

        self.logger.info("test update_user end")

    def test_3_delete_user(self):
        self.logger.info("test delete_user start")
        delete_flag, msg = self.user_service.delete_user(first_new_user_id)
        self.assertEqual(delete_flag, True)
        self.assertEqual(msg, ErrorConstant.SUCCESS)
        user_info_flag, new_user_info = self.user_service.get_user_info(first_new_user_id)
        self.assertEqual(user_info_flag, False, "被删除的用户应该是找不到的，所以获取用户信息失败")
        self.assertEqual(new_user_info, ErrorConstant.USER_IS_NOT_EXIST)
        self.logger.info("test delete_user end")

    def test_4_get_user_list(self):
        self.logger.info("test get_user_list start")
        name_map = {
            "wangmangzi": '王麻子',
            "wangwu": '王五',
            "lisi": '李四',
            "zhaoliu": '赵六'
        }
        new_user_id_list = []
        for k,v in name_map.items():
            flag, new_user_id = self.user_service.create_user({
                "username": k,
                "nickname": v,
                "password": k+"123"
            })
            self.assertEqual(flag, True)
            new_user_id_list.append(new_user_id)

        flag, user_list = self.user_service.get_user_list()
        self.assertEqual(flag, True)
        user_id_list = list(map(lambda x:x['id'], user_list))
        tmp = set(user_id_list) - set(new_user_id_list)
        self.assertEqual(len(tmp) == 0, True)
        self.logger.info("test get_user_list end")

if __name__ == '__main__':
    unittest.main()


