import datetime
import json
import time

from 测试脚本.personal.redisUtil import RedisUtil
from 测试脚本.personal.mongconnect import mongoUtil
from pymongo import MongoClient
import redis

mongoUtil = mongoUtil()
redis_db1 = RedisUtil().connect_redis()
#redis_db1= redis.Redis(host='r-2zer3tg1gl0ao7wssspd.redis.rds.aliyuncs.com',password='lFofuO80V0',db=1)

# 查询主动铃派铃记录, 主持人id anchor_id
def get_initiative_cp_bell_usage_record(anchor_id):
    initiative_cp_bell_usage_record = mongoUtil.connectMongo('couple', 'initiative_cp_bell_usage_record')
    user = mongoUtil.connectMongo('jinquan', 'user')

    #initiative_cp_bell_usage_record=MongoClient('mongodb://couple_service:aUWjzhRkIk@s-2ze804aac801b914-pub.mongodb.rds.aliyuncs.com:3717/?retryReads=false&retryWrites=false&authSource=couple')['couple']['initiative_cp_bell_usage_record']
    res = list(initiative_cp_bell_usage_record.find({'anchor_id': anchor_id}).sort([('_id', -1)]))
    if not res:
        print('未查到改小组长主动铃数据！')
        return
    for i in res:
        if i.get('status') == 0:
            status = '派铃中'
        elif i.get('status') == 1:
            status = '派铃成功'
        else:
            status = '派铃失败'
        if i.get('male_user_id'):
            user_res=user.find({'_id':i.get('male_user_id')})[0]
            print(f"{status}   男嘉宾id：{i.get('male_user_id')},昵称：{user_res.get('nick_name')}    创建时间：{i.get('create_time')}")


# 查询当前剩余主动铃
def get_current_initiative_cp_bell(anchor_id):
    key = f'couple:room:initiative_num:{anchor_id}'
    result = redis_db1.get(key)
    if result:
        print('当前剩余主动铃', result)
    else:
        print('未查询到redis中数据')


# 修改当前剩余主动铃
def set_current_initiative_cp_bell(anchor_id, value=20):
    key = f'couple:room:initiative_num:{anchor_id}'
    result = redis_db1.set(key, value)
    print(result)


# 查询剩余可兑换时间
def get_rest_time(anchor_id):
    dt = datetime.datetime.now().strftime('%Y%m%d')
    key = f'anchor:female:onmic:ts:{dt}:{anchor_id}'
    print(key)
    result = redis_db1.hget(key, 'total_seconds')
    if result:
        print(f'当前剩余时间：{result}')
    else:
        print('redis 中未查到数据！')

# 设置剩余可兑换时间，
def set_rest_time(anchor_id,value=3000):
    dt = datetime.datetime.now().strftime('%Y%m%d')
    key = f'anchor:female:onmic:ts:{dt}:{anchor_id}'
    redis_db1.hset(key, 'total_seconds', str(value))
    print('设置后的数据：',redis_db1.hgetall(key))

#获取惩罚用户（几次不抢铃 的加时惩罚）
def get_punish_user():
    key='host:dispatch_freeze_zset'
    result=redis_db1.zrange(key,start=0,end=-1)
    print(type(result),  result)
    res11=redis_db1.zrange(key,start=0,end=-1)
    print(type(res11),  res11)


if __name__ == '__main__':
    anchor_id='1452460951'  #主持人id
    shuixing='1508726511'
    yueliang='1480845661'
    get_rest_time('1561810601')
    #修改当前主动铃,value 是个数
    #et_current_initiative_cp_bell(anchor_id,value=10)

    #设置剩余可兑换时间  value是时间
    #set_rest_time(anchor_id,value=3600)
    # for i in range(50):
    #     time.sleep(20)
    #     get_rest_time(anchor_id)
    #
    # #查询主动铃派发记录
    # get_initiative_cp_bell_usage_record(anchor_id)
    # res={'code': 0, 'data': {'daily_tasks': {'description': '今日已获得', 'star': 0.0, 'tasks': [{'current_progress': 0.0, 'is_cp_game_task': False, 'star': 6.0, 'sub_title': "所有场景上麦【<font color='#FF424D'>0</font>/360】分钟", 'task_limit': False, 'task_status_desc': None, 'tips': ['统计在联盟大厅、家族大厅、小组大厅、家族语音频道、语音房、官宣房场景的上麦总时长', '上麦180分钟奖励3颗星星，每日最高可得12颗星星，每月最高可得144.0'], 'tips_title': '上麦6小时任务', 'total_progress': 360.0}, {'current_progress': 0.0, 'is_cp_game_task': False, 'star': 4.0, 'sub_title': "家族内【<font color='#FF424D'>0</font>/20】男用户晚间活动上麦30分钟", 'task_limit': False, 'task_status_desc': None, 'tips': ['每日家族活动期间(14:00-23:59)，家族内在家族大厅、小组大厅、家族语音频道上麦时长>=30分钟的男用户数量', '完成人数达10人奖励2颗星星，每日最高可得8颗星星，每月最高可得96.0颗星星'], 'tips_title': '家族内20个男用户晚间活动', 'total_progress': 20.0}], 'tips': None, 'title': '每日任务'}, 'get_monthly_advanced_tasks': {'description': '完成任务获得【2600元】奖励', 'description_url': 'https://static.diffusenetwork.com/b/2600.png', 'tasks': [{'current_progress': 0.0, 'is_cp_game_task': False, 'sub_title': '获得240.0颗星星', 'tips': None, 'total_progress': 240.0}, {'current_progress': 31288.4, 'is_cp_game_task': False, 'sub_title': '获得200000.0积分', 'tips': None, 'total_progress': 200000.0}], 'tips': ['计算通过私聊、语音房、家族等所有场景获得积分', '每月获得星星>=196.0颗时可按比例获得积分加成，获得星星>=240.0颗时，可获得满额30.0%积分加成奖励', "<font color='#FB5555'>当前积分月末可提【312.9】元</font>", "<font color='#FB5555'>当前已消耗【0.0】元</font>"], 'title': '每月收益'}, 'monthly_tasks': {'description': '本月已获得', 'description_url': 'https://static.diffusenetwork.com/b/%E5%A5%96%E5%8A%B1.png', 'star': '0.0', 'tasks': [{'current_progress': 0.0, 'is_cp_game_task': False, 'star': 20.0, 'sub_title': "组织家族参加【<font color='#FF424D'>0</font>/2】联盟PK", 'task_limit': None, 'task_status_desc': None, 'tips': ['组织家族参与联盟PK', '参与一次奖励10颗星星，每月最高可得20颗星星'], 'tips_title': '组织家族参加2次联盟PK', 'total_progress': 2.0}, {'current_progress': 0.0, 'is_cp_game_task': False, 'star': 40.0, 'sub_title': "家族内【<font color='#FF424D'>0</font>/100】人参加联盟PK，且每人活跃30分钟", 'task_limit': None, 'task_status_desc': None, 'tips': ['家族在联盟PK时家族内成员在联盟大厅活跃达30分钟次数', '仅统计本家族参与PK时活跃数据', '同一用户每天多次活跃活跃达30分钟仅计算1次', '每月达50人次时奖励20颗星星，每月最高可得40颗星'], 'tips_title': '参与联盟pk任务', 'total_progress': 100.0}], 'title': '每月任务'}, 'only_cp_task': None, 'point_rule_pic_url': 'https://static.diffusenetwork.com/poros_h5/test/index.html#/integralRule3?is_leader=1&admin_divide=1&user_divide=2&gender=2'}, 'msg': '成功'}
    # print(json.dumps(res))
    # get_punish_user()