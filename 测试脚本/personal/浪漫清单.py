import datetime
import json

import requests
from bson import ObjectId

from 测试脚本.personal.mongconnect import mongoUtil

mongoUtil = mongoUtil()

database = 'couple'

const = {
    # 游戏类型，自定义值
    '王者开黑1局': 100,
    '王者开黑5局': 101,
    '王者开黑10局': 102,
    '1局谁是卧底': 401,
    '5局谁是卧底': 402,
    '10局谁是卧底': 403,
    '3局五子棋': 604,
    '10局五子棋': 602,
    '20局五子棋': 603,
    '3局你画我猜': 704,
    '10局你画我猜': 702,
    '20局你画我猜': 703,
    '1局排雷兵': 801,
    '5局排雷兵': 802,
    '10局排雷兵': 803,
    '1局友尽闯关': 901,
    '8分钟通关友尽闯关': 910,
    '6分钟通关友尽闯关': 911,
    '1局默契对决': 1001,
    '8分钟通关默契对决': 1010,
    '6分钟通关默契对决': 1011,
    '1局狼人杀': 1101,
    '5局狼人杀': 1102,
    '10局狼人杀': 1103,
    '消消乐3局': 1202,
    '消消乐双方5w分': 1211,
    '消消乐双方10w分': 1212,
    'CP找你妹3局': 1304,
    'CP找你妹连胜5次': 1311,
    'CP找你妹连胜10次': 1312,
    '桌球1局': 1401,
    '桌球连杆3次': 1410,
    '桌球连杆5次': 1411,
    '收集齐一套嘟嘟兔宝宝' : 10221,
    '收集齐一套海豹宝宝' : 10222,
    '收集齐一套瑶瑶公主' : 10223,
    '收集齐一套跳跳猫' : 10224,
    '陪伴礼物1次' : 10500,
    '陪伴礼物6次' : 10501,
    '抱一抱3次' : 10601 ,
    '贴一贴3次' : 10701,
    '一起过纪念日' : 13051,
    '获得一个CP宝宝玩偶' : 13071
}



level_config={'lv3':'1局五子棋'}
token='23eaa43e-84a8-46af-aeb8-8ea202309f99'

romantic_list_v2_task = mongoUtil.connectMongo(database, 'romantic_list_v2_task')

def get_user_token(uid):
    user_session = mongoUtil.connectMongo('jinquan', 'user_session')
    res=user_session.find_one({'user_id':uid,'deleted':0})
    return res['session_id']



def get_romanticlist_point_reward(query):
    romanticlist_point_detail = mongoUtil.connectMongo(database, 'romanticlist_point_detail')

    now = datetime.datetime.now()
    update = {'$set': {'create_time': now, 'update_time': now}}
    result = romanticlist_point_detail.update_many(query, update)
    print(result)


def finish_lv3(b_user_id='1449736451',c_user_id='1451816241'):
    query = {'cp_unique_id': f'{b_user_id}_{c_user_id}' if b_user_id<c_user_id else f'{c_user_id}_{b_user_id}','deleted':0}
    res1 = romantic_list_v2_task.find(query)
    for i in res1:
        print('lv33  ---')
        print(i)
    res = romantic_list_v2_task.find(query)[0]
    event_type_stat = res['event_type_stat']
    print(event_type_stat)
    event_type_stat[str(const['CP找你妹3局'])] = {'count': 3}
    event_type_stat[str(const['消消乐3局'])] = {'count': 3}

    update = {'$set': {'event_type_stat': event_type_stat}}
    romantic_list_v2_task.update_many(query, update)
    update_event_inter(res['_id'],c_user_id)


# c3c：1449736451    貓貓：1452460951    火星：1406867451   水星：1452968231
# 新浪漫清单---解鎖lv5
def finish_lv5(b_user_id='1449736451',c_user_id='1451816241'):
    query = {'cp_unique_id': f'{b_user_id}_{c_user_id}' if b_user_id<c_user_id else f'{c_user_id}_{b_user_id}','deleted':0}
    res = romantic_list_v2_task.find(query)[0]
    event_type_stat = res['event_type_stat']
    print(event_type_stat)
    event_type_stat[str(const['王者开黑1局'])] = {'count': 3}
    event_type_stat[str(const['3局你画我猜'])] = {'count': 3}
    event_type_stat[str(const['桌球1局'])] = {'count': 1}
    event_type_stat[str(const['3局五子棋'])] = {'count': 3}
    event_type_stat[str(const['消消乐双方5w分'])] = {'count': 50000}

    print(event_type_stat)
    update = {'$set': {'event_type_stat': event_type_stat}}
    romantic_list_v2_task.update_many(query, update)
    update_event_inter(res['_id'],c_user_id)


def finish_lv7(b_user_id='1449736451',c_user_id='1451816241'):
    query = {'cp_unique_id': f'{b_user_id}_{c_user_id}' if b_user_id<c_user_id else f'{c_user_id}_{b_user_id}','deleted':0}
    res = romantic_list_v2_task.find(query)[0]
    event_type_stat = res['event_type_stat']
    print(event_type_stat)
    event_type_stat[str(const['10局五子棋'])] = {'count': 10}
    event_type_stat[str(const['消消乐双方5w分'])] = {'count': 50000}
    event_type_stat[str(const['王者开黑5局'])] = {'count': 5}
    event_type_stat[str(const['桌球连杆3次'])] = {'count': 3}
    event_type_stat[str(const['10局你画我猜'])] = {'count': 10}
    event_type_stat[str(const['CP找你妹连胜5次'])] = {'count': 5}
    event_type_stat[str(const['1局友尽闯关'])] = {'count': 1}
    event_type_stat[str(const['1局排雷兵'])] = {'count': 1}
    print(event_type_stat)
    update = {'$set': {'event_type_stat': event_type_stat}}
    romantic_list_v2_task.update_many(query, update)
    update_event_inter(res['_id'],c_user_id)

def finish_lv9(b_user_id='1449736451',c_user_id='1451816241'):
    query = {'cp_unique_id': f'{b_user_id}_{c_user_id}' if b_user_id<c_user_id else f'{c_user_id}_{b_user_id}','deleted':0}
    res = romantic_list_v2_task.find(query)[0]
    event_type_stat = res['event_type_stat']
    print(event_type_stat)
    event_type_stat[str(const['20局五子棋'])] = {'count': 20}
    event_type_stat[str(const['消消乐双方10w分'])] = {'count': 100000}
    event_type_stat[str(const['王者开黑10局'])] = {'count': 10}
    event_type_stat[str(const['桌球连杆5次'])] = {'count': 5}
    event_type_stat[str(const['20局你画我猜'])] = {'count': 20}
    event_type_stat[str(const['CP找你妹连胜10次'])] = {'count': 10}
    event_type_stat[str(const['8分钟通关友尽闯关'])] = {'count': 8}
    event_type_stat[str(const['5局排雷兵'])] = {'count': 5}
    event_type_stat[str(const['1局狼人杀'])] = {'count': 1}
    event_type_stat[str(const['1局默契对决'])] = {'count': 1}
    print(event_type_stat)
    update = {'$set': {'event_type_stat': event_type_stat}}
    romantic_list_v2_task.update_many(query, update)
    update_event_inter(res['_id'],c_user_id)

def finish_lv10(b_user_id='1449736451',c_user_id='1451816241'):
    query = {'cp_unique_id': f'{b_user_id}_{c_user_id}' if b_user_id<c_user_id else f'{c_user_id}_{b_user_id}','deleted':0}
    res = romantic_list_v2_task.find(query)[0]
    event_type_stat = res['event_type_stat']
    print(event_type_stat)
    event_type_stat[str(const['1局谁是卧底'])] = {'count': 1}
    event_type_stat[str(const['CP找你妹连胜10次'])] = {'count': 10}
    event_type_stat[str(const['6分钟通关友尽闯关'])] = {'count': 6}
    event_type_stat[str(const['10局排雷兵'])] = {'count': 10}
    event_type_stat[str(const['5局狼人杀'])] = {'count': 5}
    event_type_stat[str(const['收集齐一套嘟嘟兔宝宝'])] = {'count': 1}
    event_type_stat[str(const['收集齐一套海豹宝宝'])] = {'count': 1}
    event_type_stat[str(const['收集齐一套瑶瑶公主'])] = {'count': 5}
    event_type_stat[str(const['收集齐一套跳跳猫'])] = {'count': 20}
    event_type_stat[str(const['8分钟通关默契对决'])] = {'count': 8}
    print(event_type_stat)
    update = {'$set': {'event_type_stat': event_type_stat}}
    romantic_list_v2_task.update_many(query, update)
    update_event_inter(res['_id'],c_user_id)

def finish_lv11(b_user_id='1449736451',c_user_id='1451816241'):
    query = {'cp_unique_id': f'{b_user_id}_{c_user_id}' if b_user_id<c_user_id else f'{c_user_id}_{b_user_id}','deleted':0}
    res = romantic_list_v2_task.find(query)[0]
    event_type_stat = res['event_type_stat']
    print(event_type_stat)
    event_type_stat[str(const['5局谁是卧底'])] = {'count': 5}
    event_type_stat[str(const['6分钟通关默契对决'])] = {'count': 6}
    event_type_stat[str(const['10局狼人杀'])] = {'count': 10}
    event_type_stat[str(const['陪伴礼物6次'])] = {'count': 6}
    event_type_stat[str(const['抱一抱3次'])] = {'count': 3}
    event_type_stat[str(const['贴一贴3次'])] = {'count': 3}
    event_type_stat[str(const['一起过纪念日'])] = {'count': 3}
    event_type_stat[str(const['获得一个CP宝宝玩偶'])] = {'count': 3}

    print(event_type_stat)
    update = {'$set': {'event_type_stat': event_type_stat}}
    romantic_list_v2_task.update_many(query, update)
    update_event_inter(res['_id'],c_user_id)

def update_event_inter(id,uid):
    url=f'https://poros-test.diffusenetwork.com/b-k8s/ccc/romanticlist/v2/update_event?token={get_user_token(uid)}&id={id}'
    print('url;:',url)
    resp=requests.request(url=url,method='get')
    txt=json.loads(resp.text)
    if txt['code'] !=0:
        print('update task Failed!!!!')
    print(txt)




if __name__ == '__main__':
    shuixing='1508726511'
    c3c='1568323341'
    moon='1480845661'
    ge='1568103791'
    cat='1452460951'
    iq='1569006911'
    qu='1568983681'
    finish_lv3(c_user_id=qu,b_user_id=iq)


