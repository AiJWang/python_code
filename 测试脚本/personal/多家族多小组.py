import random
import time

import requests
from bson import ObjectId

from 测试脚本.personal.mongconnect import mongoUtil
from 测试脚本.personal.common import Common_Function
from 测试脚本.personal.redisUtil import RedisUtil
from 测试脚本.personal.常規 import get_nick_name
hostb='http://advanced-metis.test.diffusenetwork.net'
bpr="?pkg_name=com.hzwyst.kaituanpro&biz=kaituan&version_name=2.1.0.9&platform_name=Android&app=kaituan_leader&channel_name=unknown_channel"

maitian_bpr='?pkg_name=com.mt.maitian.pro&biz=maitian&version_name=2.1.0.9&platform_name=Android&app=maitian_leader&channel_name=unknown_channel'

hostc = 'http://advanced-poros.test.diffusenetwork.net'
redis_db1=RedisUtil().connect_redis(redis_type='jinquan')

nick_name_list=['~天空','!海鸥','@蜂鸟','%残月','^晚霞','&秋水','*长天','-物华天宝','0雄州雾列','1俊采星驰','2emmo','@天涯!',')芳草(','-千金裘-','#五花马^','~·羽化登仙']

union_info={'联盟1':'6594639g','联盟2':'6596252g','联盟3':'6597835g','联盟4':'6600251g','联盟5':'6602943g','联盟6':'6603362g','联盟7':'6605232g','联盟8':'6608115g','联盟9':'6609620g','联盟10':'6612553g','联盟11':'6613403g'}
mongoUtil = mongoUtil()

headers={'Access-Token':'0901772c-102f-4305-999f-08ef42f6400e'}

jinquan_kaituan_admin_host='https://advanced-poros-admin-test.diffusenetwork.net'

maitian_admin_host='http://porosadminsvc-maitian-test.diffusenetwork.com'

#设置redis
def set_finish(uid):
    key=f'question:finish_time:{uid}'
    res=redis_db1.set(key,'2030-04-17 16:41:51')
    print(res)

def create_user(user_type,signedRole=None,biz='kaituan'):
    if biz=='kaituan':
        url = hostc + "/service/user/register_test_account" + bpr
    else:
        url = hostc + "/service/user/register_test_account" + maitian_bpr
    if (user_type == "B"):
        user_role = 180
    else:
        user_role = 100
    print(url)
    params = {'user_role': user_role, 'nickname': random.choice(nick_name_list)+str(random.Random().randrange(20000)),
              'avatar_url': 'http://static.diffusenetwork.com/avatar/181997351.png', "age": 18, "gender": 2,'biz' : biz}
    resp = requests.get(url=url,params=params).json()
    print(resp)
    uid=resp['data']['user_info']['user_id']
    token=resp['data']['user_info']['token']
    # add_white_list(uid)
    # time.sleep(1)
    # set_finish(uid)
    # if signedRole:
    #     update_member(uid,signedRole=signedRole,biz=biz)
    # else:
    #     update_member(uid,biz=biz)
    return uid,token

def add_white_list(user_id,white_id='w_l_1170633',biz='kaituan'):
    '''加入白名单'''
    data={"white_id":white_id,"user_id":user_id}
    if biz=='kaituan':
        host=jinquan_kaituan_admin_host
    else:
        host=maitian_admin_host
    url=host+f'/vue/admin/white/add_update_white_relation?biz={biz}&pageUrl=/white_list/whiteRelation?white_id={white_id}'
    print(url)
    resp=requests.post(url=url,json=data,headers=headers).json()
    print('加入白名单：',resp)


def update_member(user_id,signedRole=10,biz='kaituan'):
    '变更家族长身份'
    if biz=='kaituan':
        host=jinquan_kaituan_admin_host
    else:
        host=maitian_admin_host
    url=host+f'/vue/admin/member/update_member?biz={biz}&pageUrl=/memberManager/list'
    #家族长 10   小组长9
    data={"userId":user_id,"act":"signedFemale","signedRole":signedRole}
    resp=requests.post(url=url,json=data,headers=headers).json()
    print('身份变更：',resp)


def create_family(union_name,family_name,family_leader_id,biz='kaituan'):
    '创建家族  union_info.get(union_name)'
    data={"family_name":family_name,"union_id":union_name,"cover_image":"http://static.diffusenetwork.com/poros_admin/img/244beeb89c10443691c93ce5325afca5.jpeg",
          "family_head":family_leader_id,"family_deputy_head_1":"","family_deputy_head_2":"","join_require":1,"city_type":1,"city_code":"","city_name":"","province_code":"",
          "cur_old_cnt":"","order_cnt":"","family_group_cnt":""}
    if biz=='kaituan':
        host=jinquan_kaituan_admin_host
    else:
        host=maitian_admin_host
    url=host+f'/vue/admin/family/add_update_family?biz={biz}&pageUrl=/groupManager/family'

    res=requests.post(json=data,url=url,headers=headers)
    print('create_family  ',res.json())

def create_family_group(family_id,family_group_name,leader_id,biz='kaituan'):
    data={"family_id":family_id,"family_group_name":family_group_name,
          "family_group_image":"http://static.diffusenetwork.com/poros_admin/img/d71a23bceeb34a14a4ac400393e4fcc6.jpeg","group_user_id":"",
          "leader_id":leader_id,"group_leader_id":""}
    if biz=='kaituan':
        host=jinquan_kaituan_admin_host
    else:
        host=maitian_admin_host
    url=host+f'/vue/admin/family_group/create_family_group?biz={biz}&pageUrl=/groupManager/cpList'

    res=requests.post(json=data,url=url,headers=headers)
    print('create_family_group  ',res.json())

def create_union(name,biz='kaituan'):
    if biz=='kaituan':
        host=jinquan_kaituan_admin_host
    else:
        host=maitian_admin_host
    url=host+f'/vue/admin/family_active/add_update_union?biz={biz}'
    data={"name":name,"icon":"https://static-maitian.diffusenetwork.com/poros_admin/img/4c7bf16a61bb4461bdda0b5490932e9e.jpg",
          "banner":"https://static-maitian.diffusenetwork.com/poros_admin/img/5f8eda1116a04796bffddb5f67f56263.jpg","is_test_union":True,"category":"pmd","desc":""}
    res=requests.post(json=data,url=url,headers=headers)
    print('create_union  ',res.json())

def get_family_id_by_name(family_name):
    family=mongoUtil.connectMongo('jinquan','family')
    family_info=list(family.find({'family_name':family_name}))[0]
    print('family_info: ',family_info)
    return family_info.get('_id')

def add_to_family(user_id,family_id):
    url=f'https://advanced-poros-admin-test.diffusenetwork.net/vue/admin/family/add_user_into_family?biz=kaituan&pageUrl=/groupManager/family&family_id={family_id}&target_user_id={user_id}&user_id='
    resp=requests.get(url=url,headers=headers).json()
    print('加入家族: ',resp)


def add_to_family_group():
    url='https://advanced-poros-admin-test.diffusenetwork.net/vue/admin/family_group/update_family_group?biz=kaituan&pageUrl=/groupManager/cpList'


def get_female_user(*args):
    couple_level_relation=mongoUtil.connectMongo('jinquan','couple_level_relation')
    result=list(couple_level_relation.find({'$or':[{'female_user_id':args[0],'male_user_id':args[1]},{'female_user_id':args[1],'male_user_id':args[0]}]}).sort([('_id',-1)]))[0]
    if i:=result:
        print(f'female_uid:{i.get("female_user_id")}, 昵称： {get_nick_name(i.get("female_user_id"))}, 创建时间: {i.get("create_time")}')
    else:
        print('未查到相关记录')

def get_belong_info(*args):
    '查询归属关系'
    cp_belong_relation=mongoUtil.connectMongo('organization_service_test','cp_belong_relation')
    res=None
    #,'deleted': 0
    if args:
        res=list(cp_belong_relation.find({'$or':[{'user_ids_key':f'{args[0]}_{args[1]}','deleted': 0},{'user_ids_key':f'{args[1]}_{args[0]}','deleted': 0}]}).sort([('_id',-1)]))
    if not res:
        print(f'{args[0]}与{args[1]} 无归属')
        return
    for i in list(res):
        print(i)
        print(f'归属小组长id：{i.get("group_leader_id")}，小组长昵称: {get_nick_name(i.get("group_leader_id"))}')


def insert_into_belong(times):
    i=0
    id=ObjectId('664f0344e9319cda0dcf60d3')
    cp_belong_relation=mongoUtil.connectMongo('organization_service_test','cp_belong_relation')
    res=list(cp_belong_relation.find({'_id':id}))[0]
    res.pop('_id')
    print(res)
    while i<times:
        buid,btoken=create_user('B')
        cuid,ctoken=create_user('C')
        user_ids_key=f'{buid}_{cuid}' if buid>cuid else f'{cuid}_{buid}'
        res['user_ids_key']=user_ids_key
        res['user_ids']=[buid,cuid]
        i+=1
        print(res)
        cp_belong_relation.insert_one(res)
        print(res)
        time.sleep(1)

def get_main_family(uid=None):
    '查主小组家族'
    url=hostb+'/user/info'+bpr
    requst_data={
        "source": "mine_fragment",
        "token": Common_Function().get_token(uid)
    }
    result=requests.post(url=url,json=requst_data).json()
    main_union_name=result.get('data').get('user_info').get('union_name')
    main_family_name=result.get('data').get('user_info').get('family_name')
    main_family_id=result.get('data').get('user_info').get('family_id')
    main_family_group_id=result.get('data').get('user_info').get('family_group_id')
    joined_family_group_ids=result.get('data').get('user_info').get('joined_family_group_ids')
    joined_family_ids=result.get('data').get('user_info').get('joined_family_ids')
    joined_union_ids=result.get('data').get('user_info').get('joined_union_ids')
    family=mongoUtil.connectMongo('jinquan','family')
    print(result)
    #'family_type':4 是小组
    main_family_group_name=''
    if main_family_group_id:
        main_family_group_name= list(family.find({'_id':main_family_group_id,'family_type':4}))[0].get('family_name')
    print(f'主联盟名称：{main_union_name}')
    print(f'主家族id: {main_family_id}，主家族名称：{main_family_name}\n主小组id: {main_family_group_id}，主小组名称：{main_family_group_name}')
    print(f'加入联盟个数: {len(joined_union_ids)}\n加入联盟列表: {joined_union_ids}')
    print(f'加入家族个数: {len(joined_family_ids)}\n加入家族列表: {joined_family_ids}')
    group_name_list=list(map(lambda main_family_group_id: list(family.find({'_id':main_family_group_id,'family_type':4}))[0].get('family_name'),joined_family_group_ids))
    print(f'加入小组个数：{len(joined_family_group_ids)}，\n加入小组名称：{group_name_list}')
    print(f'加入小组列表: {joined_family_group_ids}')
    print(result)

if __name__ == '__main__':
    user_info={'cat':'1711839501','huoxing':'1737355881','moon':'1681374311','water':'1737124861','c3c':'1719532071','nier':'1712763671',
               'sunflower':'1713620141','qu':'879461741','qingwa':'1722967701','sun':'1736859731','ge':'1723904651','iq':'1723929671'}
    #get_main_family('1681374311')
    user=user_info.get('c3c')
    # for i in range(2,11):
    #     create_union(f'aj-测试联盟{i}','maitian')
    # moon_list=['23184411','23241721','23297761','23367321','23412101']
    # i=4
    # uid=moon_list[i]
    # get_female_user(user,user_info.get('sun'))
    set_finish(user)
    add_white_list(user,biz='kaituan')
    # get_belong_info(user,user_info.get('sun'))
    get_main_family(uid=user)
    #insert_into_belong(1)
    # for i in range(1,5):
    #     add_to_family(user,get_family_id_by_name(f'家族1联盟{i}'))

