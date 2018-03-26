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

