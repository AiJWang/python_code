#coding=gb2312

from 测试脚本.personal.redisUtil import RedisUtil

redis_db1=RedisUtil().connect_redis()
ss={'rmb-10': '0', 'rmb-50': '1', 'rmb-100': '1', 'rmb-300': '1', 'rmb-500': '3'}

def hget(uid='1758059141'):
    key=f'point_exchange_tims:2024-06-06:{uid}'
    res=redis_db1.hgetall(key)
    print(res)
    redis_db1.hset(key,'rmb-10', 0)
    res=redis_db1.hgetall(key)
    print(res)

if __name__ == '__main__':
    hget()