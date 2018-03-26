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
    