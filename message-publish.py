#encoding:utf-8
from messagehelper import RedisHelper

if __name__ == '__main__':
    helper = RedisHelper()
    helper.publish('people', 'hello,world')
    helper.publish('people', 'World needs a better understanding of China')
    helper.publish('people', 'China’s central bank to recall fourth set of RMB')
    helper.publish('people','exit')

