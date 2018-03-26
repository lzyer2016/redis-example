#encoding:utf-8
from messagehelper import RedisHelper

if __name__ == '__main__':
    helper = RedisHelper()
    helper.subscribe('people')