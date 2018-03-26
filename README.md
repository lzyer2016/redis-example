# Redis的简单实例
## 游戏玩家积分排行榜
```python
# encoding:utf-8
import redis
import uuid
import random

total_size = 20
key = '游戏名：奔跑吧，阿里！'
def get_redis_conn():
    pool = redis.ConnectionPool(host='x.x.x.x', port=6379, db=0, password='x')
    conn = redis.StrictRedis(connection_pool=pool)
    return conn
def init_game_data():
    conn = get_redis_conn()
    #清除之前的数据
    conn.delete(key)
    players = []
    for i in range(total_size):
        players.append(uuid.uuid4())
    
    for uid in players:
        score = random.randint(0, 500)
        conn.zadd(key, score, uid)
    result = conn.zrange(key, 0, -1, withscores=True)
    for item in result:
        print('uid=%s, score=%s' %(item[0], item[1]))
def rank_game_data():
    conn = get_redis_conn()
    result = conn.zrevrange(key, 0, -1, withscores=True)
    print('全部玩家排行榜')
    for item in result:
        print('uid=%s, score=%s' %(item[0], item[1]))
    print('Top5玩家')
    result = conn.zrevrange(key, 0, 4, withscores=True)
    for item in result:
        print('uid=%s, score=%s'%(item[0], item[1]))
    print('评分在200-300的用户')
    result = conn.zrangebyscore(key, 200, 300, withscores=True)
    for item in result:
        print('uid=%s, score=%s'%(item[0], item[1]))

if __name__ == '__main__':
    init_game_data()
    rank_game_data()
```
## 网上商城商品相关性分析
```python
# encoding:utf-8
import redis
import uuid
import random

# 产品列表
keys = ["阿里云:产品:啤酒", "阿里云:产品:巧克力", "阿里云:产品:可乐",
        "阿里云:产品:口香糖", "阿里云:产品:牛肉干", "阿里云:产品:鸡翅"]
def get_redis_conn():
    pool = redis.ConnectionPool(host='x', port=6379, db=0,  password='x')
    conn = redis.StrictRedis(connection_pool=pool)
    return conn
def init_relation_data():
    conn = get_redis_conn()
    # 清楚key
    for key in keys:
        conn.delete(key)
    # 模拟购物
    for i in range(0, 6):
        custom_shop(i, conn)
def custom_shop(i, conn):
    bought = random.randint(0, 3)
    if bought == 0:
        print('用户%d购买了%s,%s,%s' %(i, keys[0], keys[2], keys[1]))
        conn.zincrby(keys[0], keys[1], 1)
        conn.zincrby(keys[0], keys[2], 1)
        conn.zincrby(keys[1], keys[0], 1)
        conn.zincrby(keys[1], keys[2], 1)
        conn.zincrby(keys[2], keys[0], 1)
        conn.zincrby(keys[2], keys[1], 1)
    elif bought == 2:
        print('用户%s购买了%s,%s,%s' %(i, keys[4], keys[2], keys[3]))
        conn.zincrby(keys[4], keys[2], 1)
        conn.zincrby(keys[4], keys[3], 1)
        conn.zincrby(keys[3], keys[4], 1)
        conn.zincrby(keys[3], keys[2], 1)
        conn.zincrby(keys[2], keys[4], 1)
        conn.zincrby(keys[2], keys[3], 1)
    elif bought == 0:
        print('用户%s购买了%s,%s,%s' %(i, keys[1], keys[5]))
        conn.zincrby(keys[5], keys[1], 1)
        conn.zincrby(keys[1], keys[5], 1)
def relation_data():
    conn = get_redis_conn()
    for key in keys:
        print('>>>与%s一起购买的商品有<<<'%(key))
        related_list = conn.zrevrange(key, 0, 0, withscores=True)
        #print(related_list)
        for key, value in related_list:
           print('商品名称:%s,共购买次数%s' %(key, value))

if __name__ =='__main__':
    #init_relation_data()
    relation_data()
```
## 消息发布与订阅
```python
#encoding:utf-8
import redis

class RedisHelper:
    '''
        以"__"开头表示私有的
    '''
    def __init__(self):
        pool = redis.ConnectionPool(host='x.x.x.x', port=6379, db=0,  password='x')
        self.__conn = redis.StrictRedis(connection_pool = pool)
    def publish(self, channel, message):
        self.__conn.publish(channel, message)
        return True
    def subscribe(self, channel):
        pub = self.__conn.pubsub()
        pub.subscribe(channel)
        pub.parse_response()
        print('start receive message')
        while True:
            message = pub.parse_response()
            print('receive=%s' %(message)) # message[message, channel, content]
            if message[2] == 'exit':
                break
```
发布者：  
```python
#encoding:utf-8
from messagehelper import RedisHelper
if __name__ == '__main__':
    helper = RedisHelper()
    helper.publish('people', 'hello,world')
    helper.publish('people', 'World needs a better understanding of China')
    helper.publish('people', 'China’s central bank to recall fourth set of RMB')
    helper.publish('people','exit')
```
订阅者:  
```python
#encoding:utf-8
from messagehelper import RedisHelper

if __name__ == '__main__':
    helper = RedisHelper()
    helper.subscribe('people')
```
## 管道传输
```python
#encoding:utf-8
import redis
import time

count = 5000 #操作次数
key = 'KVStore'
def get_redis_conn():
    pool = redis.ConnectionPool(host='x.x.x.x', port=6379, db=0,  password='x')
    conn = redis.StrictRedis(connection_pool=pool)
    return conn
def no_pipeline_task():
    conn = get_redis_conn()
    conn.delete(key)
    start = int(time.time()) 
    for i in range(0, 5000):
        conn.incr(key)
    end = int(time.time())
    print('no_pipeline time=%s' %(end-start))
def use_pipeline_task():
    conn = get_redis_conn()
    conn.delete(key)
    start = int(time.time()) 
    pipe = conn.pipeline()
    for i in range(0, 5000):
        pipe.incr(key)
    pipe.execute()
    end = int(time.time())
    print('use_pipeline time=%s' %(end-start))

if __name__ == '__main__':
    use_pipeline_task()
    no_pipeline_task()
'''
测试结果
use_pipeline time=2
no_pipeline time=223
'''
```
## 事务处理
```python
#encoding:utf-8
import redis
import sys

key ='tx_key'
def get_redis_conn():
    pool = redis.ConnectionPool(host='x', port=6379, db=0,  password='x')
    conn = redis.StrictRedis(connection_pool=pool)
    return conn
if __name__ =='__main__':
    conn = get_redis_conn()
    conn.delete(key)
    pipe = conn.pipeline()
    try:
        pipe.multi() #开启事务
        pipe.incr(key)
        pipe.incr(key)
        #a = 1/0  # 模拟异常，事务不会被提交
        pipe.incr(key)
        pipe.execute() #提交事务
    except Exception as err:
        print(err)
        pass
    print('val=%s' %(conn.get(key)))
```
参考:  
[阿里云Redis最佳实战](https://help.aliyun.com/document_detail/26366.html?spm=a2c4g.11186623.6.599.7JUSTx)
