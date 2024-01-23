import datetime
import time

import requests

from 测试脚本.personal.mongconnect import mongoUtil
from 测试脚本.personal.redisUtil import RedisUtil

mongoUtil = mongoUtil()

redis_db1=RedisUtil().connect_redis()


# 修改恩爱值
def update_love_socre(male_user_id, inter_user_id, love_score=299):
    couple_relation = mongoUtil.connectMongo('jinquan', 'couple_relation')
    query = {'male_user_id': male_user_id, 'internal_user_id': inter_user_id}
    ress = couple_relation.find(query)
    for i in ress:
        print(i)
    value = {'$set': {'love_score': love_score}}
    res = couple_relation.update_many(query, value)

    print(res.modified_count)


# 修改互动值
def update_interactive_value(male_user_id, inter_user_id, value=30):
    couple_relation = mongoUtil.connectMongo('jinquan', 'couple_relation')
    query = {'male_user_id': male_user_id, 'internal_user_id': inter_user_id}
    ress = couple_relation.find(query)
    for i in ress:
        print(i)
    value = {'$set': {'interactive_value': value}}
    res = couple_relation.update_many(query, value)
    print('修改条数', res.modified_count)


# 查询互动值
def get_interactive_value(male_user_id, inter_user_id):
    couple_relation = mongoUtil.connectMongo('jinquan', 'couple_relation')
    user_ids_key = f'{inter_user_id}_{male_user_id}' if male_user_id > inter_user_id else f'{male_user_id}_{inter_user_id}'
    query = {'user_ids_key': user_ids_key}
    ress = couple_relation.find_one(query)
    if ress:
        print('互动值为：', ress.get('interactive_value'))
        return ress.get('interactive_value')
    else:
        print('未查询到相关数据~')
        return None


# 修改cp陪伴礼物   盲盒
def update_blind_box(cuid, buid, num=0):
    c_p_blind_box = mongoUtil.connectMongo('jinquan', 'c_p_blind_box')
    cp_tag = f'{buid}_{cuid}' if cuid > buid else f'{cuid}_{buid}'
    query = {'cp_tag': cp_tag}
    res=c_p_blind_box.update_many(query, {'$set': {'cnt': num,'gift_list':[[211, 78, 212]]}})
    print(f'修改了 {res.modified_count} 条数据')


# 修改金虎数量
def update_golden_tigers(uid, num=0):
    user_attach = mongoUtil.connectMongo('jinquan', 'user_attach')
    user_attach.update_many({'_id': uid}, {'$set': {'golden_tigers': num}})


# 判断房间类型
def get_room_type(familyid='',anchor_id=''):
    # 3/5人房 rtc_service
    if familyid:
        family = mongoUtil.connectMongo('jinquan', 'family')
        result = list(family.find({'_id': familyid}))
        if result:
            im_room_id = result[0].get('im_room_id')
            if im_room_id:
                if str(im_room_id).startswith('tx') or str(im_room_id).startswith('TX'):
                    print('家族场景，房间类型为腾讯：', im_room_id)
                    return im_room_id
                else:
                    print('家族场景，房间类型为云信：', im_room_id)
            else:
                print('im_room_id获取失败！！！！')
        else:
            print('查不到对应家族！！')
    elif anchor_id:
        couple_room = mongoUtil.connectMongo('rtc_service', 'couple_room')
        result = list(couple_room.find({'anchor': anchor_id}))
        if result:
            im_room_id = result[0].get('im_room_id')
            if im_room_id:
                if str(im_room_id).lower().startswith('tx'):
                    print('家族场景，房间类型为腾讯：', im_room_id)
                    return im_room_id
                else:
                    print('家族场景，房间类型为云信：', im_room_id)
            else:
                print('im_room_id获取失败！！！！')
        else:
            print('未找到主持人房间信息')
    else:
        print('请传入家族id或者3/5人房主持人id')

#修改充能值
def update_user_game_energy(user_list,value):
    for user in user_list:
        if(redis_db1.exists(f'user_game_energy:{user}')):
            print('修改前：',redis_db1.hgetall(f'user_game_energy:{user}'))
            redis_db1.hset(f'user_game_energy:{user}','energy',value)
            print('修改后：',redis_db1.hgetall(f'user_game_energy:{user}'))

        else:
            print('请先开始一局游戏！')

if __name__ == '__main__':
    #update_blind_box('1489653311','1072719101',3)
    #火星：1490781851     我们的歌：1489653311    iqoo:1488701421   yueliang:1480845661  shuixing:1508726511
    #update_love_socre('1509680431','1508726511')
    update_interactive_value('1510063171','1508726511')