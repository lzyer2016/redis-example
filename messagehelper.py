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