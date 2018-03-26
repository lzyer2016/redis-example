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



