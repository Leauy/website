#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
@author: leauy
'''
import traceback
import time
import pdb
import pymysql
from configparser import ConfigParser
from DBUtils.PooledDB import PooledDB
from blog.const.config import DB_INI_PATH


class _ScheDb(object):
    def __init__(self):
        configparser = ConfigParser()
        configparser.read(DB_INI_PATH, encoding='UTF-8')
        username = configparser.get('db', 'username')
        password = configparser.get('db', 'password')
        database = configparser.get('db', 'database')
        host = configparser.get('db', 'host')
        port = int(configparser.get('db', 'port'))
        self.pool = self.__init_pool(username, password, database, host, port)

    def __init_pool(self, username, password, database, host, port, connection_size=5):
        """
        初始化数据库连接池
        :param username:
        :param password:
        :param database:
        :param host:
        :param port:
        :param connection_size:
        :return:
        """
        pool = None
        try:
            retry_count = 5
            while True:
                if retry_count == 0:
                    break
                try:
                    pool = PooledDB(pymysql,
                                    maxconnections=connection_size,
                                    user=username,
                                    host=host,
                                    passwd=password,
                                    port=port,
                                    db=database)
                    break
                except Exception as e:
                    retry_count -= 1
                time.sleep(3)
        except:
            traceback.print_exc()
        return pool

    def get_conn(self):
        """
        获取数据库连接
        :return:
        """
        flag = True
        num = 0
        conn = None
        while flag:
            try:
                conn = SchedDbConn(self.pool.connection())
                flag = False
            except:
                traceback.print_exc()
                time.sleep(0.5)
                num += 1
                if num > 5:
                    raise Exception("can not connect MYSQL")
        return conn

class SchedDbConn(object):
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def select(self,sql, params=None, dict_ret=True):
        result = []
        def convert(x):
            return x.strip() if type(x) == str else x
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            if dict_ret:
                for row in self.cursor.fetchall():
                    tmp_result = {}
                    for i, value in enumerate(row):
                        tmp_result[self.cursor.description[i][0].strip()] = convert(value)
                    result.append(tmp_result)
            else:
                result = self.cursor.fetchall()
            return result
        except:
            traceback.print_exc()
            raise Exception(traceback.format_exc())

    def execute(self, sql, params=None, auto_commit=False):
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            if auto_commit:
                self.commit()
        except:
            print (sql)
            self.rollback()
            traceback.print_exc()

    def fetchall(self):
        data = []
        try:
            data = self.cursor.fetchall()
        except:
            traceback.print_exc()
        return data

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

SchedDB = _ScheDb()

if __name__ == '__main__':
    configparser = ConfigParser()
    configparser.read(DB_INI_PATH, encoding='UTF-8')
    username = configparser.get('db', 'username')
    password = configparser.get('db', 'password')
    database = configparser.get('db', 'database')
    host = configparser.get('db', 'host')
    port = int(configparser.get('db', 'port'))
    conn = pymysql.connect(user=username,passwd=password,port=port,db=database,host=host)
    cursor = conn.cursor()
    cursor.execute("select * from user")
    result = cursor.fetchall()
    for i in result:
        print( i)

    conn = SchedDB.get_conn()
    print (conn.select("select * from user where id in (%s)", (1,)))


