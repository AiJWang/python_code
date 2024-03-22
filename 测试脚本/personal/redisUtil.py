import json

import redis

from util.yamlUtil import YmlTuil


class RedisUtil:
    redis_info=YmlTuil().readYml(path='../../config.yml').get('redis',None)
    host= redis_info.get('host')
    auth= redis_info.get('auth')
    db=redis_info.get('db')
    redis_online_room=YmlTuil().readYml(path='../../config.yml').get('redis_online_room_settings',None)
    def connect_redis(self):
        return redis.Redis(host=self.host,password=self.auth,db=self.db,decode_responses=True)

    def connect_redis_online_room(self):
        print(self.redis_online_room.get('host'),self.redis_online_room.get('auth'), self.redis_online_room.get('db'), self.redis_online_room.get('port'))
        return redis.Redis(host=self.redis_online_room.get('host'), password=self.redis_online_room.get('auth'), db=self.redis_online_room.get('db'), port=self.redis_online_room.get('port') ,decode_responses=True)

    def queryListData(self,key):
        redis=self.connect_redis()
        return redis.get(key)

if __name__=='__main__':
    # re=RedisUtil()
    # platfor='cp_bell_test_female_ids'
    # ress=re.queryListData(platfor)
    # print(ress,type(ress))
    print('ss123s'.isascii())


