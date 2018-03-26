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
