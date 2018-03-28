# encoding:utf-8
import redis
import time
import multiprocessing
'''
    一个简单的抢购Demo
'''
def get_redis_conn():
    pool = redis.ConnectionPool(host='x', port=6379, db=0,  password='x')
    conn = redis.StrictRedis(connection_pool=pool)
    return conn

def service(i):
    conn = get_redis_conn()
    key ='iphonex'
    #使用lua脚本来控制原子性
    script = '''
                local remain = redis.call('get', KEYS[1])
                if tonumber(remain) >0 then
                    redis.call('decr', ARGV[1])
                    return remain
                else
                    return remain
                end
                '''
    getstock  = conn.register_script(script)
    ret = getstock(keys=[key], args=[key])
    if int(ret) > 0:
        print('%s get it success '%(i))
        return True
    else:
        print('%s sold out'%(i))
        return False

if __name__ == "__main__":
    conn = get_redis_conn()
    conn.set('iphonex', 7) #设置 7台iphoneX
    for i in range(100): #100个抢购者
        p = multiprocessing.Process(target=service, args=(i,))
        p.start()
       



