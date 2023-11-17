import json

import redis

from util.yamlUtil import YmlTuil


class RedisUtil:
    redis_info=YmlTuil().readYml(path='../../config.yml').get('redis',None)
    host= redis_info.get('host')
    auth= redis_info.get('auth')
    db=redis_info.get('db')
    def connect_redis(self):
        return redis.Redis(host=self.host,password=self.auth,db=self.db)

    def queryListData(self,key):
        redis=self.connect_redis()
        return redis.get(key)

if __name__=='__main__':
    re=RedisUtil()
    platfor='cp_bell_test_female_ids'
    ress=re.queryListData(platfor)
    print(ress,type(ress))


