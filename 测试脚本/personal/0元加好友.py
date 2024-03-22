from 测试脚本.personal.mongconnect import mongoUtil
from 测试脚本.personal.redisUtil import RedisUtil
from 测试脚本.personal.女嘉宾积分相关 import del_signed_voice_female_monthly
from 测试脚本.personal.常規 import del_friend_relation, update_interactive_value

mongoUtil=mongoUtil()
redis_db1=RedisUtil().connect_redis()


#同一个房间家好友缓存:video_room:friend


def update_user_send_zero_gift_record(uid,receiver_uid_list=[],delete=0):
    user_send_zero_gift_record=mongoUtil.connectMongo('jinquan','user_send_zero_gift_record')
    result = list(user_send_zero_gift_record.find({'user_id': uid}))

    if delete and len(result):
        user_record = result[0]
        male_send_user_ids = list(user_record.get('male_send_user_ids', None))
        print('male_send_user_ids',male_send_user_ids)
        user_send_zero_gift_record.delete_one({'user_id':uid})
        #删好友关系
        for i in male_send_user_ids:
            del_friend_relation(uid,i)
            video_room_friend = f'video_room:friend:{uid}:{i}'
            redis_db1.delete(video_room_friend)
    elif receiver_uid_list:
        #删除好友关系
        for i in receiver_uid_list:
            del_friend_relation(uid,i)
            video_room_friend = f'video_room:friend:{uid}:{i}'
            redis_db1.delete(video_room_friend)
        if len(result):
            user_record=result[0]
            male_send_user_ids=user_record.get('male_send_user_ids',None)
            if male_send_user_ids:
                male_send_user_ids=set(male_send_user_ids)-set(receiver_uid_list)
                count=user_send_zero_gift_record.update_one({'user_id':uid},{'$set':{'male_send_user_ids':list(male_send_user_ids)}}).modified_count
                print('修改条数：',count)

        else:
            print('未查到数据~')
    else:
        for i in user_send_zero_gift_record.find({'user_id':uid}):
            print(i)




if __name__ == '__main__':

    cat='1452460951'
    water='1508726511'
    moon='1480845661'
    womendege='1518022851'
    qu='1518313741'
    c3c='1520053481'
    #删除女嘉宾积分
    receiver_uid_list = [cat, water, moon,qu]
    receiver_uid_list = [womendege]
    for i in receiver_uid_list:
        del_signed_voice_female_monthly(i,delete=1)
        update_interactive_value(c3c,i,30)
    update_user_send_zero_gift_record(c3c,delete=1)
