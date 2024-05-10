import datetime
import time

import redis
import requests
from pymongo import MongoClient

from 测试脚本.personal.mongconnect import mongoUtil
from 测试脚本.personal.redisUtil import RedisUtil

mongoUtil = mongoUtil()

redis_db1=RedisUtil().connect_redis()

'''
说明：两个b端组cp，唯一ccp积分池表 jackpot  用的是一条记录，区分了送戒指人的积分池积分和被送戒指人的积分池积分
1. 先修改jackpot的创建时间到很久以前
2. 结算的时候修改收戒指人 jackpot_daily_task 里面的数据， no_accompany_days ：连续几天未完成任务。必须有一条前天的数据，才能执行扣减。如果是下发，则不必

实验组：只改redis就行
1. set together_mic::1496686331_938314521:2024-01-13 1（设置是否共同上麦）
2. set CACHE:DAILY:INTERACTION:TIME:2024-01-18:1387212431_1464897431 10000 （设置单日互动值）

'''

#唯一cp积分池
def get_jackpoint(uid):
    jackpot = mongoUtil.connectMongo('jinquan', 'jackpot')
    result=jackpot.find({'receiver_id':uid,'status':'PENDING'})[0]
    print('b收礼人积分池数量: ',result.get('score'))
    return result.get('_id')

#唯一cp积分池 更新时间
def update_jackpoint_create_time(uid,value=None):
    jackpot = mongoUtil.connectMongo('jinquan', 'jackpot')
    if value:
        result = jackpot.update_many({'receiver_id': uid, 'status': 'PENDING'},
                                     {'$set': value})
        print('唯一cp积分池修改：',result.modified_count)
    else:
        result=jackpot.update_many({'receiver_id':uid,'status':'PENDING'},{'$set':{'create_time':datetime.datetime(2024, 1, 2, 19, 31, 21, 943000)}})
        print('唯一cp积分池创建时间修改',result.modified_count)


#共同上麦时长
def get_together_on_mic(uid,femaluid,date='',delete=0,seconds=0):
    uid_key=f'{uid}_{femaluid}' if uid<femaluid else f'{femaluid}_{uid}'
    if date:
        key = f'CACHE:DAILY:TOGETHER:MIC:TIME:{date}:{uid_key}'
    else:
        key=f'CACHE:DAILY:TOGETHER:MIC:TIME:{datetime.datetime.today().strftime("%Y%m%d")}:{uid_key}'
    print(key)
    if delete:
        redis_db1.delete(key)
    else:
        result=redis_db1.get(key)
        print(result)
    if seconds:
        res=redis_db1.set(key,seconds)
        print(res)

#设置互动时长
def set_hudong(uid,femaluid,date='2024-01-18',value=1800):
    uid_key = f'{uid}_{femaluid}' if uid < femaluid else f'{femaluid}_{uid}'
    key=f'CACHE:DAILY:INTERACTION:TIME:{date}:{uid_key}'
    res=redis_db1.set(key,value)
    print(res)


#连麦记录
def set_lianmai_record(uid,femaluid,date,delete=1):
    uid_key = f'{uid}_{femaluid}' if uid < femaluid else f'{femaluid}_{uid}'
    key=f'together_mic::{uid_key}:{date}'
    if delete and redis_db1.exists(key):
        res=redis_db1.delete(key)
        print('连麦记录：',res)
    else:
        print(redis_db1.set(key,1))

#删除扣减弹窗的缓存
def del_tanchaung(uid):
    key=f'only_cp_accompany_task:{uid}:{datetime.datetime.today().strftime("%Y%m%d")}'
    if redis_db1.exists(key):
        res=redis_db1.delete(key)
        print('扣减弹窗：',res)


#触发结算
def settle_cp(uid,femaluid):
    uid_key = f'{uid}_{femaluid}' if uid < femaluid else f'{femaluid}_{uid}'
    redis_db1.delete(f'jackpot:task:{uid_key}:2024-01-20')
    jackpot_daily_task = mongoUtil.connectMongo('jinquan', 'jackpot_daily_task')
    jackpot_daily_task.delete_many({'receiver_id':femaluid,'date':datetime.datetime(2024, 1, 20, 00, 00, 00, 000000)})
    url=f'http://metis-test.diffusenetwork.com/test_tools/settle_jackpot_task?jackpot_id={get_jackpoint(femaluid)}'
    result=requests.request(method='get',url=url)
    print(result.text)
    print(result.json())

def duizhaozu(c_uid,female_uid):
    #修改积分池创建时间
    update_jackpoint_create_time(female_uid)
    #修改积分池积分
    update_jackpoint_create_time(female_uid,value={'score':1000})
    #设置共同上麦时间
    get_together_on_mic(c_uid, female_uid, seconds=180, date='20240120')
    #删除缓存的弹窗
    del_tanchaung(female_uid)
    #触发结算（需要先有一条前天的记录，可直接触发一次结算，修改时间）
    settle_cp(c_uid,female_uid)

def shiyanzu(c_uid,female_uid):
    #修改积分池创建时间
    update_jackpoint_create_time(female_uid)
    # 修改积分池积分 bb组cp需要增加 sender_score
    update_jackpoint_create_time(female_uid,value={'sender_score':1000,'score':1000})

    date_list=['2024-01-19','2024-01-20','2024-01-18']
    #修改互动时长
    for date in date_list:
        set_hudong(c_uid,female_uid,date=date,value=10)
    #设置连麦记录
    set_lianmai_record(c_uid,female_uid,'2024-01-20')
    set_lianmai_record(c_uid,female_uid,'2024-01-21',delete=0)
    #删除缓存的弹窗
    del_tanchaung(female_uid)
    #触发结算（需要先有一条前天的记录，可直接触发一次结算，修改时间）
    settle_cp(c_uid,female_uid)

if __name__ == '__main__':
    # id=get_jackpoint('1508200921')
    # print(id)
    # 对照组 水星：1508726511     C3C：1498619021    火星：1508472331   我们的歌：1489653311  月亮 1480845661
    female_uid='1480845661'
    c_uid='1578800521'
    #get_together_on_mic(c_uid, female_uid, seconds=180, date='20240120')
    set_hudong(c_uid,female_uid,date='2024-03-27')