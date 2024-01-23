
import datetime

from 测试脚本.personal.mongconnect import mongoUtil

mongo = mongoUtil()

# 根据c端用户id，修改组cp申请的发起时间，超过24h自动退款（定时任务执行的30min 一次，搜索的是 24h-27h之间过期的）
def update_create_time():
    couple_level_relation = mongo.connectMongo('jinquan', 'couple_level_relation')
    query = {'male_user_id': {'$in': ['1074951301', '1381183141']}, 'progress_status': 'female'}
    # 获取昨天的当前时刻
    time = datetime.datetime.now() - datetime.timedelta(days=7,hours=23, minutes=59, seconds=59)
    str_time = time.strftime('%Y-%m-%d %H:%M:%S')
    print(str_time, type(str_time))
    update = {'$set': {'create_time': str_time}}
    couple_level_relation.update_many(query, update)
    result = couple_level_relation.find(query)
    for i in result:
        print(type(i['create_time']), i)
