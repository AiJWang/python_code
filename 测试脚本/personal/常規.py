import datetime
import time


from 测试脚本.personal.mongconnect import mongoUtil
from 测试脚本.personal.redisUtil import RedisUtil

mongoUtil = mongoUtil()

redis_db1=RedisUtil().connect_redis()
'''
如何成为老的家族长和小组长：
1.user_attach表:更改sign_start_time 为2022.07.26 11：00：00 前
2.sign_role_record表：更改create_time 为2022.07.26 11：00：00 前
3.更改redis
   key:
   user:sign_role:first:ts:{user_id}:{role}
   value:
   将时间戳时间戳为2022.07.26 11：00：00 前
'''

'''修改签约时间，user-attach'''
def get_nick_name(uid):
    '''获取用户昵称'''
    user = mongoUtil.connectMongo('jinquan', 'user')
    result=list(user.find({'_id':uid}))[0]
    return result.get('nick_name')

def update_sign_time_groupld_familyld(uid,is_family_leader=False,sign_old=True):
    '''修改家族长小组长签约时间，变家族长小组长'''
    next_role=9
    stime='2022-07-20 11:00:00'
    if is_family_leader:
        next_role=10
    if not sign_old:
        stime='2023-07-20 11:00:00'
    target_time=datetime.datetime.strptime(stime,'%Y-%m-%d %H:%M:%S')
    user_attach = mongoUtil.connectMongo('jinquan', 'user_attach')
    uas=user_attach.update_one({'_id':uid},{'$set':{'sign_start_time':target_time}})
    print(f'user attach 更新时间：{uas.modified_count}')
    sign_role_record = mongoUtil.connectMongo('jinquan', 'sign_role_record')
    slr=sign_role_record.update_one({'user_id':uid,'next_role':next_role},{'$set':{'create_time':target_time}})
    print(f'sign_role_record 更新时间：{slr.modified_count}')
    times=int(time.mktime(target_time.timetuple()))
    key=f'user:sign_role:first:ts:{uid}:{next_role}'
    redis_res=redis_db1.set(key,str(times))
    print(redis_res)


def update_love_socre(male_user_id, inter_user_id, love_score=299):
    '''修改恩爱值'''
    couple_relation = mongoUtil.connectMongo('jinquan', 'couple_relation')
    query = {'male_user_id': male_user_id, 'internal_user_id': inter_user_id}
    ress = couple_relation.find(query)
    for i in ress:
        print(i)
    value = {'$set': {'love_score': love_score}}
    res = couple_relation.update_many(query, value)

    print(res.modified_count)

def update_unsigned_female_point(uid,account):
    '''修改未签约女嘉宾积分总额及当日积分'''
    user_account = mongoUtil.connectMongo('account','user_account')
    res=user_account.update_one({'_id':uid},{'$set':{'point':int(account)}})
    print(res.modified_count)
    today=datetime.datetime.now().date()
    key=f'user_today_incr_point:{uid}:{today}' #今日获得积分
    redis_db1.set(key,f'{account}')

def update_unsigned_female_on_imc_time(uid,total_time=18000):
    '''修改女嘉宾上麦时长'''
    if type(total_time)!=int:
        total_time=int(total_time)
    user_attach = mongoUtil.connectMongo('jinquan', 'user_attach')
    res=user_attach.update_one({'_id':uid},{'$set':{'total_on_mic_duration':total_time}})
    print(res.modified_count)

def update_sign_start_time(uid,sign_time=datetime.datetime.now()-datetime.timedelta(days=datetime.datetime.now().day-1)):
    '''修改签约时间，默认为当月1号'''
    user_attach = mongoUtil.connectMongo('jinquan', 'user_attach')
    ress=user_attach.update_one({'_id':uid},{'$set':{'sign_start_time':sign_time}})
    print(ress.modified_count)



def update_interactive_value(male_user_id, inter_user_id, value=30):
    '''修改互动值'''
    couple_relation = mongoUtil.connectMongo('jinquan', 'couple_relation')
    query = {'male_user_id': male_user_id, 'internal_user_id': inter_user_id}
    ress = couple_relation.find(query)
    for i in ress:
        print(i)
    value = {'$set': {'interactive_value': value}}
    res = couple_relation.update_many(query, value)
    print('修改条数', res.modified_count)


def get_interactive_value(male_user_id, inter_user_id):
    '''查询互动值'''
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

def update_blind_box(cuid, buid, num=3):
    '''修改cp陪伴礼物   盲盒'''
    c_p_blind_box = mongoUtil.connectMongo('jinquan', 'c_p_blind_box')
    cp_tag = f'{buid}_{cuid}' if cuid > buid else f'{cuid}_{buid}'
    query = {'cp_tag': cp_tag,'user_id':cuid}
    res=c_p_blind_box.update_many(query, {'$set': {'cnt': num,'gift_list':[[211, 78, 212]]}})
    if not res.modified_count:
        data={'biz': 'jinquan', 'app': 'jinquan_leader',
              'expire_time': datetime.datetime.now(),
              'user_id': cuid, 'cp_user_id': buid,
              'cp_tag': cp_tag,
              'cnt': num, 'create_time': datetime.datetime.now(),
              'gift_list': [[175, 87, 78], [174, 78, 44], [212, 87, 174]],
              'zero_discount_opportunity': 0,
              'three_discount_opportunity': 0}

        ins_resu=c_p_blind_box.insert_one(data)
        print(f'插入数据{ins_resu.inserted_id}条')
    else:
        print(f'修改了 {res.modified_count} 条数据')
    query = {'cp_tag': cp_tag,'user_id':buid}
    res=c_p_blind_box.update_many(query, {'$set': {'cnt': num,'gift_list':[[211, 78, 212]]}})
    if not res.modified_count:
        data={'biz': 'jinquan', 'app': 'jinquan_leader',
              'expire_time': datetime.datetime.now(),
              'user_id': buid, 'cp_user_id': cuid,
              'cp_tag': cp_tag,
              'cnt': num, 'create_time': datetime.datetime.now(),
              'gift_list': [[175, 87, 78], [174, 78, 44], [212, 87, 174]],
              'zero_discount_opportunity': 0,
              'three_discount_opportunity': 0}

        ins_resu=c_p_blind_box.insert_one(data)
        print(f'插入数据{ins_resu.inserted_id}条')
    else:
        print(f'修改了 {res.modified_count} 条数据')



def update_golden_tigers(uid, num=1):
    '''修改金虎数量'''
    user_attach = mongoUtil.connectMongo('jinquan', 'user_attach')
    res=user_attach.update_many({'_id': uid}, {'$set': {'golden_tigers': num}})
    print(res.modified_count)

def update_golden_tigers_maitian(user_id,cp_user_id,num=3):
    '''修改金虎数量'''
    gold_dragon = mongoUtil.connectMongo('maitian','gold_dragon', db='backpack')
    cp_tag=f'{user_id}_{cp_user_id}' if cp_user_id>user_id else f'{cp_user_id}_{user_id}'
    print(cp_tag)
    data_dict={'biz': 'maitian', 'app': 'maitian',
               'user_id': user_id,
               'cp_user_id': cp_user_id,
               'cp_tag': cp_tag,
               'dragon_num': num, 'deleted': 0,
               'create_time': datetime.datetime.now(),
               'update_time': datetime.datetime.now(),
               'delete_time': datetime.datetime(1970, 1, 1, 0, 0)}
    res=list(gold_dragon.find({'user_id':user_id,'cp_user_id':cp_user_id}))
    if res:
        count=gold_dragon.update_many({'user_id':user_id,'cp_user_id':cp_user_id}, {'$set': {'dragon_num': num}}).modified_count
        print(f'count:{count}')
    else:
        ss=gold_dragon.insert_one(data_dict).inserted_id
        print(f'插入数据{ss}')

def get_room_type(familyid='',anchor_id=''):
    '''判断房间类型'''
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


def update_user_game_energy(user_list,value):
    '''修改充能值'''
    for user in user_list:
        if(redis_db1.exists(f'user_game_energy:{user}')):
            print('修改前：',redis_db1.hgetall(f'user_game_energy:{user}'))
            redis_db1.hset(f'user_game_energy:{user}','energy',value)
            print('修改后：',redis_db1.hgetall(f'user_game_energy:{user}'))

        else:
            print('请先开始一局游戏！')


def del_friend_relation(uid,friend_uid=None):
    '''删除好友关系'''
    user_friend = mongoUtil.connectMongo('organization_service_test', 'user_friend')
    if friend_uid:
        rows=user_friend.delete_many({'$or':[{'user_id':uid,'friend_id':friend_uid},{'user_id':friend_uid,'friend_id':uid}]}).deleted_count
    else:
        rows=user_friend.delete_many({'user_id':uid}).deleted_count
    print(f'删除用户好友关系 {rows} 条')


def del_female_guest_point_record(uid_list,delete=0):
    '''查询明细&删除积分'''
    female_guest_point_record = mongoUtil.connectMongo('account', 'female_guest_point_record')
    res_female_guest_point_record=[]
    for uid in uid_list:
        res=list(female_guest_point_record.find({'user_id': uid}).sort([('_id', -1)]).limit(1))
        if res:
            res_female_guest_point_record.append(res[0])
    if res_female_guest_point_record and not delete:
        return res_female_guest_point_record
    rows=female_guest_point_record.delete_many({'user_id':{'$in':uid_list}}).deleted_count
    print(f'删除明细条数 {rows} 条')


def update_register_version_and_time(uid,register_version=None,register_time=None):
    '''修改用户注册时间及注册版本'''
    if register_time or register_version:
        update_info={}
        if register_time:
            update_info['register_datetime']=register_time
            if '-' in register_time:
                register_date_time=datetime.datetime.strptime(register_time,'%Y-%m-%d %H:%M:%S')
                register_time=int(time.mktime(register_date_time.timetuple())* 1000.0 + register_date_time.microsecond / 1000.0)
                print(type(register_time),register_time)
            update_info['register_time']=str(register_time)
        if register_version:
            update_info['register_version']=register_version
        if update_info:
            user = mongoUtil.connectMongo('jinquan', 'user')
            res=user.update_one({'_id':uid},{'$set':update_info})
            print(res.modified_count)
            print(update_info)
    else:
        print('注册版本及注册时间为空，不进行更新操作！')



if __name__ == '__main__':
    #设置旧白银清单  register_time='2023-01-01 12:01:23',register_version='2.0.4.7'
    #sgfh   95-99  对照组
    # update_unsigned_female_point('1642724051',4000)
    # ss=sign_time=datetime.datetime.now()-datetime.timedelta(days=datetime.datetime.now().day-1)
    # print(ss,type(ss))
    # update_sign_start_time('1642724051')
    time1="2024-06-03 19:33:24"
    time2="2024-06-03 19:33:25"
    ss=time1.split(':')
    ss1=time2.split(':')
    print(ss[0]+ss[1])
    print(ss[0]+ss[1]==ss1[0]+ss1[1])
    print(time2>time1)
    print(time1[0:-3])
    print(datetime.datetime.strptime(time1,'%Y-%m-%d %H:%M:%S'))
    # update_unsigned_female_on_imc_time('1760777471')
    #update_sign_start_time('1760777471')
    # user_info={'qingwa':'29942421','cat':'28632441','moon':'29907791'}
    # update_golden_tigers_maitian('29942421','29907791')
    #update_golden_tigers('1881119701',num=3)
    update_blind_box('1881119701','1880857211',10)