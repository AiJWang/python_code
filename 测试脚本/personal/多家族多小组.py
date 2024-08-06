import random
import time

import requests
from bson import ObjectId

from 测试脚本.personal.mongconnect import mongoUtil
from 测试脚本.personal.common import Common_Function
from 测试脚本.personal.redisUtil import RedisUtil
from 测试脚本.personal.常規 import get_nick_name, update_love_socre

hostb='http://advanced-metis.test.diffusenetwork.net'
bpr="?pkg_name=com.hzwyst.kaituanpro&biz=kaituan&version_name=2.1.0.9&platform_name=Android&app=kaituan_leader&channel_name=unknown_channel"

maitian_bpr='?pkg_name=com.mt.maitian&biz=maitian&version_name=2.1.1.5&platform_name=Android&app=maitian&channel_name=unknown_channel'

smeng_bpr='?pkg_name=com.rswl.smengpro&biz=smeng&version_name=2.1.1.5&platform_name=Android&app=smeng_leader&channel_name=unknown_channel'

hostc = 'http://advanced-poros.test.diffusenetwork.net'

maitian_hostb = 'http://metis-maitian-test.diffusenetwork.com'

maitian_hostc = 'http://poros-maitian-test.diffusenetwork.com'

redis_db1=RedisUtil().connect_redis(redis_type='jinquan')

bpr_list={'kaituan':bpr,'smeng':smeng_bpr,'maitian':maitian_bpr}

nick_name_list=['~天空','!海鸥','@蜂鸟','%残月','^晚霞','&秋水','*长天','-物华天宝','0雄州雾列','1俊采星驰','2emmo','@天涯!',')芳草(','-千金裘-','#五花马^','~·羽化登仙']

union_info={'联盟1':'6639077g','联盟2':'6642780g','联盟3':'6643874g','联盟4':'6646382g','联盟5':'6648667g','联盟6':'6650969g','联盟7':'6652170g','联盟8':'6653810g','联盟9':'6656953g','联盟10':'6658757g','联盟11':'6660027g'}
mongoUtil = mongoUtil()

headers={'Access-Token':'dc2f290f-ca52-4e82-955b-d37096d7ce9d'}

jinquan_kaituan_admin_host='https://advanced-poros-admin-test.diffusenetwork.net'

maitian_admin_host='http://porosadminsvc-maitian-test.diffusenetwork.com'

#设置redis
def set_finish(uid):
    key=f'question:finish_time:{uid}'
    res=redis_db1.set(key,'2030-04-17 16:41:51')
    print(res)



def create_user(user_type,signedRole=None,biz='kaituan'):
    if biz == 'maitian':
        url=maitian_hostc+"/service/user/register_test_account" + bpr_list.get(biz)
    else:
        url=hostc+"/service/user/register_test_account" + bpr_list.get(biz)
    if user_type == "B":
        user_role = 180
    else:
        user_role = 100
    print(url)
    #https://static-maitian.diffusenetwork.com/b/avatar/xiaozhushou.png
    #http://static.diffusenetwork.com/avatar/181997351.png
    params = {'user_role': user_role, 'nickname': random.choice(nick_name_list)+str(random.Random().randrange(20000)),
              'avatar_url': 'http://static-maitian.diffusenetwork.com/b/avatar/xiaozhushou.png', "age": 18, "gender": 2,'biz' : biz}
    print(params)
    resp = requests.get(url=url,params=params).json()
    print(resp)
    uid=resp['data']['user_info']['user_id']
    token=resp['data']['user_info']['token']
    # add_white_list(uid,biz='smeng')
    # time.sleep(1)
    # set_finish(uid)
    if user_type == "B":
        if signedRole==9:
            update_member(uid,signedRole=signedRole,biz=biz)
        elif signedRole==10:
            update_member(uid,biz=biz)
        else:
            update_member(uid,signedRole=6,biz=biz)
    return uid,token

def add_white_list(user_id,white_id='w_l_1170633',biz='kaituan'):
    '''加入白名单'''
    data={"white_id":white_id,"user_id":user_id}
    if biz=='maitian':
        host=maitian_admin_host
    else:
        host=jinquan_kaituan_admin_host
    url=host+f'/vue/admin/white/add_update_white_relation?biz={biz}&pageUrl=/white_list/whiteRelation?white_id={white_id}'
    print(url)
    resp=requests.post(url=url,json=data,headers=headers).json()
    print('加入白名单：',resp)


def update_member(user_id,signedRole=10,biz='kaituan'):
    '变更家族长身份'
    if biz=='maitian':
        host=maitian_admin_host
    else:
        host=jinquan_kaituan_admin_host
    url=host+f'/vue/admin/member/update_member?biz={biz}&pageUrl=/memberManager/list'
    #家族长 10   小组长9
    data={"userId":user_id,"act":"signedFemale","signedRole":signedRole}
    resp=requests.post(url=url,json=data,headers=headers).json()
    print('身份变更：',resp)


def create_family(union_name,family_name,family_leader_id,biz='kaituan'):
    '创建家族  union_info.get(union_name)'
    data={"family_name":family_name,"union_id":union_info.get(union_name),"cover_image":"http://static.diffusenetwork.com/poros_admin/img/244beeb89c10443691c93ce5325afca5.jpeg",
          "family_head":family_leader_id,"family_deputy_head_1":"","family_deputy_head_2":"","join_require":1,"city_type":1,"city_code":"","city_name":"","province_code":"",
          "cur_old_cnt":"","order_cnt":"","family_group_cnt":""}
    if biz=='maitian':
        host=maitian_admin_host
    else:
        host=jinquan_kaituan_admin_host
    url=host+f'/vue/admin/family/add_update_family?biz={biz}&pageUrl=/groupManager/family'
    res=requests.post(json=data,url=url,headers=headers)
    print('create_family  ',res.json())

def create_family_group(family_id,family_group_name,leader_id,biz='kaituan'):
    data={"family_id":family_id,"family_group_name":family_group_name,
          "family_group_image":"http://static.diffusenetwork.com/poros_admin/img/d71a23bceeb34a14a4ac400393e4fcc6.jpeg","group_user_id":"",
          "leader_id":leader_id,"group_leader_id":""}
    if biz=='maitian':
        host=maitian_admin_host
    else:
        host=jinquan_kaituan_admin_host
    url=host+f'/vue/admin/family_group/create_family_group?biz={biz}&pageUrl=/groupManager/cpList'

    res=requests.post(json=data,url=url,headers=headers)
    print('create_family_group  ',res.json())

def create_union(name,biz='kaituan'):
    if biz=='maitian':
        host=maitian_admin_host
    else:
        host=jinquan_kaituan_admin_host
    url=host+f'/vue/admin/family_active/add_update_union?biz={biz}'
    data={"name":name,"icon":"https://static-maitian.diffusenetwork.com/poros_admin/img/4c7bf16a61bb4461bdda0b5490932e9e.jpg",
          "banner":"https://static-maitian.diffusenetwork.com/poros_admin/img/5f8eda1116a04796bffddb5f67f56263.jpg","is_test_union":True,"category":"pmd","desc":""}
    res=requests.post(json=data,url=url,headers=headers)
    print('create_union  ',res.json())

def get_family_id_by_name(family_name,biz):
    if biz=='maitian':
        family=mongoUtil.connectMongo('maitian','family',db='poros')
    else:
        family=mongoUtil.connectMongo('jinquan','family')
    family_info=list(family.find({'family_name':family_name,'biz':biz}))[0]
    print('family_info: ',family_info)
    return family_info.get('_id')

def add_to_family(user_id,family_id,biz='smeng'):
    if biz=='maitian':
        url=f'{maitian_admin_host}/vue/admin/family/add_user_into_family?biz={biz}&pageUrl=/groupManager/family&family_id={family_id}&target_user_id={user_id}&user_id='
    else:
        url=f'{jinquan_kaituan_admin_host}/vue/admin/family/add_user_into_family?biz={biz}&pageUrl=/groupManager/family&family_id={family_id}&target_user_id={user_id}&user_id='
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

def get_main_family(uid=None,biz='smeng'):
    '查主小组家族'
    url=hostb+'/user/info'+bpr_list.get(biz)
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
    user_info={'cat':'1806998831','c3c':'1806645441','maoer':'1807071741','water':'1812440201','nier':'1807522711','sunflower':'1807723721','qingwa':'1808420971',
               'moon':'1797576921','huoxing':'1808107121','iq':'1812422201'}
    biz='maitian'
    uid,token=create_user('B',biz=biz)
    print(uid,token)
    # #34868411 127bc584-b9a3-4e20-bbda-bcf459c8a9d3
    # # 家族1积分自动化	,家族2积分自动化
    family_id=get_family_id_by_name('家族1积分自动化',biz=biz)
    add_to_family(uid,family_id,biz=biz)
    # create_family_group(family_id,'F2_G1_B10',uid,biz=biz)