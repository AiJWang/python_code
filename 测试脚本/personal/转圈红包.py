
from 测试脚本.personal.redisUtil import RedisUtil

redis_db1=RedisUtil().connect_redis()

#获取红包圈数
def get_redpack_circle_cum(user_id,day_age):
    key=f'circle_reward:v2:{user_id}:{day_age}'
    print(key)
    result=redis_db1.get(key)
    print(result)



if __name__ == '__main__':
    get_redpack_circle_cum('1639584671',0)