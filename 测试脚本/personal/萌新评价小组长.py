import datetime
import json

import requests
from bson import ObjectId

from 测试脚本.personal.mongconnect import mongoUtil

mongoUtil=mongoUtil()

#查询联盟下小组长人数
def get_leader_member(unionid):
    family = mongoUtil.connectMongo(0, 'jinquan', 'family')
    queryFamily = {'union_id': unionid}
    familyResultList = family.find(queryFamily)
    familyList = list()
    for i in familyResultList:
        familyList.append(i['_id'])
    print(familyList)
    queryleader = {'$and': [{'family_id': {'$in': familyList}}, {'deleted': 0}, {'is_leader': True}]}

    family_group_member = mongoUtil.connectMongo(0, 'jinquan', 'family_group_member')
    result1 = family_group_member.find(queryleader)
    res = list(result1)
    for i in res:
        print(i)
    print(len(res))

#根据得分排序
def get_score(element):
    return element['union_ranking']

def query_union_leader_score(unionid,reverse):
    mx_comment = mongoUtil.connectMongo(1, 'ugc', 'mx_comment_stat')
    query = {'union_id':unionid,'date':datetime.datetime.today().strftime('%Y-%m-%d')}

    result = mongoUtil.queryData(mx_comment, query)
    res=list(result)
    res.sort(key=get_score,reverse=reverse)
    for i in res:
        #print(i)
        print(i['group_leader_id'],i['score'],i['star'],i['union_ranking'])
    print(len(res))
    return res

taiyang={'familyid':'97798139','userid':'1379982171','unionid':'6501a1e5922bb81b0ff46491','token':'a8569e89-257c-4eba-971e-570cb7fb22ce'}
maomao={'userid':'1381571261'}
huoxing={'userid':'1387058641'}
#评价数据插入
def insert_mx_comment():
    mx_comment = mongoUtil.connectMongo(1, 'ugc', 'mx_comment')
    query={'group_leader_id': '1002985161'}
    result = mongoUtil.queryData(mx_comment, query)
    data = dict(result[0])
    now=datetime.datetime.now()
    #data['comment'] = 'good girl'
    print(data)
    for i in range(10):
        data.pop('_id')
        data.pop('create_time')
        data.pop('update_time')
        data['family_id'] = taiyang['familyid']
        data['group_leader_id'] = '943405281'
        data['union_id'] = taiyang['unionid']
        data['create_time'] = now
        data['update_time'] = now
        data['stars'] = 3
        mongoUtil.insertData(mx_comment, data)

def update_topN(n,union_id):
    mx_comment = mongoUtil.connectMongo(1, 'ugc', 'mx_comment')
    res=query_union_leader_score(union_id,False)
    for i in range(n):
        query = {'group_leader_id': res[i]['group_leader_id']}
        result=dict(mx_comment.find(query)[0])
        result.pop('_id')
        result['stars']=4
        mongoUtil.insertData(mx_comment, result)
    #删除之前的数据
    remove_info={'union_id': union_id, 'date': '2023-10-26', 'union_ranking': {'$lte': n}}
    mx_comment_stat = mongoUtil.connectMongo(1, 'ugc', 'mx_comment_stat')
    mx_comment_stat.delete_many(remove_info)

def update_daoshuN(n,union_id):
    mx_comment = mongoUtil.connectMongo(1, 'ugc', 'mx_comment')
    res=query_union_leader_score(union_id,False)
    for i in range(n):
        leader_id=res[i]['group_leader_id']
        print('daoshu',leader_id)
        query = {'group_leader_id': leader_id}
        update = {'$set': {'stars': 5}}
        mx_comment.update_many(query,update)


#更新任务
def update_task():
    #删除任务 '1379982171'
    theme_task = mongoUtil.connectMongo(0, 'jinquan', 'theme_task')
    query={'task_type':'family_group_leader_mx_comment','user_id':{'$in':['1379982171','943405281','1381571261']},'deleted':0}
    update = {'$set': {'deleted': 1}}
    theme_task.update_many(query,update)
    result=list(theme_task.find(query))
    if(len(result)==0):
        print('任务状态删除成功------------')
    #重新设置任务
    url='http://metis-test.diffusenetwork.com/b-k8s/bbb/theme_task/mx_comment_create_task?biz=jinquan&app=jinquan_leader'
    header={'X-TOKEN':taiyang['token'],'Content-Type': 'application/json;charset=UTF-8'}
    data={"user_ids": ['943405281']}  #'1379982171','1387058641',
    resp=requests.request(method='post',url=url,headers=header,data=json.dumps(data))
    print(resp)
    print(resp.text)
    result=json.loads(resp.text)
    print(resp)
    print(resp.status_code)
    if (resp.status_code==200&result['code']==0&result['msg']=='ok'):
        print('任务更新成功------------')
    print(result)
#get_leader_member('649bdd48f2d8217b0ad35c48')

#query_union_leader_score('6501a1e5922bb81b0ff46491')

#update_topN(55,'6445ec3df7420bcf9f0c41b1')

#天平不平 6445ec3df7420bcf9f0c41b1

#update_daoshuN(29,'6445ec3df7420bcf9f0c41b1')


#insert_mx_comment()


update_task()
