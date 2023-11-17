import json

import redis

class RedisUtil:
    host='r-2zer3tg1gl0ao7wssspd.redis.rds.aliyuncs.com'
    auth='lFofuO80V0'
    db=1
    def connect_redis(self):
        return redis.Redis(host=self.host,password=self.auth,db=self.db)

    def queryListData(self,key):
        redis=self.connect_redis()
        res=redis.get(key)
        print(res)
        return res

if __name__=='__main__':
    re=RedisUtil()
    platfor='mx_comment_platform_ranklist_20231013-20231015'
    union='mx_comment_union_ranklist_20231013-20231015_615015c215703a6fd28e39d4'
    ress=re.queryListData(platfor)
    list=json.loads(ress)
    for i in list:
        print(i)
    print('-'*20)
    unionrank=re.queryListData(union)
    for i in json.loads(unionrank):
        print(i)

