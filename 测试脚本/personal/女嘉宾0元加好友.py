import random

from 测试脚本.personal.mongconnect import mongoUtil
from 测试脚本.personal.redisUtil import RedisUtil

mongodb = mongoUtil()
redis_db1 = RedisUtil().connect_redis()


# 修改男用户已绑定次数
def update_user_self_add_zero_friend_times(uid,num):
    user_send_zero_gift_record = mongodb.connectMongo('jinquan', 'user_send_zero_gift_record')
    res = user_send_zero_gift_record.find({'user_id': uid})
    if res:
        user_record=list(res)[0]
        male_send_user_ids=user_record.get('male_send_user_ids')
        if len(male_send_user_ids) < num:
            for i in range(num-len(male_send_user_ids)):
                male_send_user_ids.append(str(generate_random_num(6)))
            update_info=user_send_zero_gift_record.update_one({'user_id': uid},{'$set':{'male_send_user_ids':male_send_user_ids}})
            print(update_info.modified_count)
        print(user_record)

def del_redis(uid):
    redis_key=f'user:prize:xing_yun_yong_hu:{uid}'
    res=redis_db1.delete(redis_key)
    print(res)


def update_female_times(uid,num):
    user_send_zero_gift_record = mongodb.connectMongo('jinquan', 'user_send_zero_gift_record')
    res = user_send_zero_gift_record.find({'user_id': uid})
    if res:
        user_record=list(res)[0]
        bind_male_ids=user_record.get('bind_male_ids')
        if num==0:
            bind_male_ids=[]
        else:
            if len(bind_male_ids) < num:
                for i in range(num-len(bind_male_ids)):
                    bind_male_ids.append(str(generate_random_num(6)))
        update_info=user_send_zero_gift_record.update_one({'user_id': uid},{'$set':{'bind_male_ids':bind_male_ids,'bind_males':num}})
        print(update_info.modified_count)


#生成指定位数随机数
def generate_random_num(num):
    min=10**(num-1)
    max=(10**num)-1
    return random.randint(min,max)

if __name__ == '__main__':
    womendege='1589507791'
    cat='1452460951'
    # update_user_self_add_zero_friend_times(womendege,5)
    # del_redis(womendege)
    update_female_times(cat,0)