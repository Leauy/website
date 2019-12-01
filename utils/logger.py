#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
@author: leauy
'''
import logging
import os
import configparser
from blog.const.config import LOGDIR_PATH, LOGFILE_PATH
def getLogger():
    if not os.path.isdir(LOGDIR_PATH):
        os.mkdir(LOGDIR_PATH)
        f = open(LOGFILE_PATH, 'w')
        f.close()

    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.DEBUG)
    handler = logging.FileHandler(LOGFILE_PATH)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - pid(%(thread)d)  %(pathname)s %(funcName)s- '
                                  '%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(console)


    return logger

if __name__ == '__main__':
    logger = getLogger()
    logger.info('sbsb')
    logger.debug('sbsb')
    logger.warning('sbsb')
    logger.error('sbsb')