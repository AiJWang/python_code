import datetime

import pytest
import requests

from 测试脚本.personal.common import Common_Function
from 测试脚本.personal.女嘉宾积分相关 import del_signed_voice_female_monthly
from 测试脚本.personal.常規 import del_female_guest_point_record,update_blind_box,update_sign_time_groupld_familyld
from 测试脚本.personal.mongconnect import mongoUtil


mongoUtil = mongoUtil()
cat ='1452460951'
moon ='1480845661'
hostb='http://advanced-metis.test.diffusenetwork.net'
bpr="?pkg_name=com.liquid.poros.pro&biz=jinquan&version_name=2.1.0.9&platform_name=Android&app=jinquan_leader&channel_name=unknown_channel"

hostc='http://advanced-poros.test.diffusenetwork.net'
cpr='?pkg_name=com.liquid.poros&biz=jinquan&version_name=2.1.0.9&platform_name=Android&app=jinquan&channel_name=unknown_channel'

def get_main_family(uid=None):
    '查主小组家族'
    user=mongoUtil.connectMongo('jinquan','user')
    userinfo=list(user.find({'_id':uid}))[0]
    if userinfo.get('app')=='jinquan_leader':
        url=hostb+'/user/info'+bpr
    else:
        url=hostc+'/service/user/info'+cpr
    requst_data={
        "source": "mine_fragment",
        "token": Common_Function().get_token(uid)
    }
    result=requests.post(url=url,json=requst_data).json()
    main_family_id=result.get('data').get('user_info').get('family_id')
    main_family_group_id=result.get('data').get('user_info').get('family_group_id')
    return main_family_group_id,main_family_id
# flDouble 家族长双份     glSingle： 小组长单分
def cal_point(sender,receiver,anchor=None,scene='room'):
    receiver_group_leader_money = 0
    sender_family_leader_money = 0
    receiver_family_leader_money = 0
    sender_group_leader_money = 0
    anchor_changdifei = 0
    user=mongoUtil.connectMongo('jinquan','user')
    sender_user_info=list(user.find({'_id':sender}))
    sender_app_info=sender_user_info[0].get('app')
    #根据送装扮记录表，查询礼物价格
    prop_send_record = mongoUtil.connectMongo('jinquan', 'prop_send_record')
    prop_send_record_newest=list(prop_send_record.find({'user_id':sender}).sort([('_id', -1)]).limit(1))
    if sender_app_info=='jinquan_leader':
        coin=prop_send_record_newest[0].get('price_total')-prop_send_record_newest[0].get('deduct_freecoin')
    else:
        coin=prop_send_record_newest[0].get('price_total')
    gift_sender_time=prop_send_record_newest[0].get('create_time')
    time_range=[gift_sender_time-datetime.timedelta(seconds=2),gift_sender_time+datetime.timedelta(seconds=2)]
    receiver_point = coin*10*0.15
    family=mongoUtil.connectMongo('jinquan','family')

    sender_group_id,sender_family_id=get_main_family(sender)
    reveiver_group_id,reveiver_family_id=get_main_family(receiver)

    sender_group_leader_id=list(family.find({'_id':sender_group_id}))[0].get('family_head')
    sender_family_leader_id=list(family.find({'_id':sender_family_id}))[0].get('family_head')
    couple_relation_unique=mongoUtil.connectMongo('jinquan','couple_relation_unique')
    cps=list(couple_relation_unique.find({'$or':[{'user_id':sender,'bind_user_id':receiver,'deleted':0},{'user_id':receiver,'bind_user_id':sender,'deleted':0}]}))

    if sender_group_id==reveiver_group_id:
        receiver_group_leader_id= sender_group_leader_id
        receiver_family_leader_id=sender_family_leader_id
    else:
        receiver_group_leader_id= list(family.find({'_id':reveiver_group_id}))[0].get('family_head')
        receiver_family_leader_id=list(family.find({'_id':reveiver_family_id}))[0].get('family_head')

    #收礼人积分池
    receiver_pool_point=round(coin*10*0.05,2)
    female_guest_point_record=del_female_guest_point_record({receiver,sender_group_leader_id,sender_family_leader_id,receiver_group_leader_id,receiver_family_leader_id,anchor})
    familyratio=0.01
    if scene=='family':
        groupratio=0.035
    elif scene== 'chat':
        groupratio=0
        familyratio=0
        if cps and sender_app_info =='jinquan':
            receiver_pool_point=receiver_pool_point*1.2
            receiver_point=receiver_point*1.2
    else:
        groupratio=0.017

    #家族长管理费
    receiver_family_leader_money+=coin*10*familyratio
    sender_family_leader_money+=coin*10*familyratio

    # 小组长管理费
    receiver_group_leader_money+=coin*10*groupratio
    sender_group_leader_money+=coin*10*groupratio

    #场地费
    if anchor:
        anchor_changdifei+=coin*10*0.1

    #自己收无场地费
    if receiver==anchor:
        anchor_changdifei=0

    total_group_money=None
    total_family_money=None
    if anchor == receiver_group_leader_id:
        receiver_group_leader_money+=anchor_changdifei
    elif anchor == sender_group_leader_id:
        sender_group_leader_money+=anchor_changdifei
    elif anchor ==sender_family_leader_id:
        sender_family_leader_money+=anchor_changdifei
    elif anchor == receiver_family_leader_id:
        receiver_family_leader_money+=anchor_changdifei

    if sender_group_id==reveiver_group_id:
        total_group_money=receiver_group_leader_money+sender_group_leader_money
        total_family_money=receiver_family_leader_money+sender_family_leader_money
    else:
        if sender_family_id == reveiver_family_id:
            total_family_money=receiver_family_leader_money+sender_family_leader_money
    if total_group_money:
        res=f'收礼人积分: {round(receiver_point,2)}\n收礼人积分池积分: {round(receiver_pool_point,2)}\n家族长总计：{round(total_family_money,2)}\n小组长总计: {round(total_group_money,2)}\n主持人场地费: {anchor_changdifei}'
    else:
        res=f'收礼人积分: {round(receiver_point,2)}\n收礼人积分池积分: {round(receiver_pool_point,2)}\n收礼人家族长总计：{round(receiver_family_leader_money,2)}\n收礼人小组长总计: {round(receiver_group_leader_money,2)}\n' \
            f'送礼人家族长总计：{round(sender_family_leader_money,2)}\n' \
            f'送礼人小组长总计: {round(sender_group_leader_money,2)}\n主持人场地费: {anchor_changdifei}'

    print(res)
    print('-'*30)

    if total_group_money:
        for i in female_guest_point_record:
            if i.get('user_id')==receiver_group_leader_id:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(total_group_money,2) ==0, '小组长 积分报错啦！！'
                    print('收礼人小组长 积分测试通过')
                else:
                    assert total_group_money==0, f'小组长积分报错啦，应得积分：{total_group_money}，实际获得：0'
                    print('收礼人小组长 积分测试通过')
            elif i.get('user_id')==receiver_family_leader_id:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(total_family_money,2) ==0, '家族长 积分报错啦！！'
                    print('收礼人家族长 积分测试通过')
                else:
                    assert total_family_money==0, f'家族长积分报错啦，应得积分：{total_family_money}，实际获得：0'
                    print('收礼人家族长 积分测试通过')
            elif i.get('user_id')==receiver:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(receiver_point,2) ==0, '收礼人 积分报错啦！！'
                    print('收礼人 积分测试通过')
                else:
                    assert receiver_point==0, f'收礼人积分报错啦，应得积分：{receiver_point}，实际获得：0'
                    print('收礼人 积分测试通过')
    else:
        for i in female_guest_point_record:
            if i.get('user_id')==receiver_group_leader_id:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(receiver_group_leader_money,2) ==0, '收礼人小组长 积分报错啦！！'
                    print('收礼人小组长 积分测试通过')
                else:
                    assert receiver_group_leader_money==0, f'收礼人小组长积分报错啦，应得积分：{receiver_group_leader_money}，实际获得：0'
                    print('收礼人小组长 积分测试通过')
            elif i.get('user_id')==sender_group_leader_id:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(sender_group_leader_money,2) ==0, '送礼人小组长 积分报错啦！！'
                    print('送礼人小组长  积分测试通过')
                else:
                    assert round(sender_group_leader_money,2) ==0, '送礼人小组长 积分报错啦！！'
                    print('送礼人小组长  积分测试通过')
            elif i.get('user_id')==receiver_family_leader_id:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(receiver_family_leader_money,2) ==0, '收礼人家族长 积分报错啦！！'
                    print('收礼人家族长  积分测试通过')
                else:
                    assert round(receiver_family_leader_money,2) ==0, '收礼人家族长 积分报错啦！！'
                    print('收礼人家族长  积分测试通过')
            elif i.get('user_id')==sender_family_leader_id:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(sender_family_leader_money,2) ==0, '送礼人家族长 积分报错啦！！'
                    print('送礼人家族长 积分测试通过')
                else:
                    assert round(sender_family_leader_money,2) ==0, '送礼人家族长 积分报错啦！！'
                    print('送礼人家族长 积分测试通过')
            elif i.get('user_id')==receiver:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(receiver_point,2) ==0, '收礼人 积分报错啦！！'
                    print('收礼人 积分测试通过')
                else:
                    assert round(receiver_point,2) ==0, '收礼人 积分报错啦！！'
                    print('收礼人 积分测试通过')

    #积分池
    receiver_jackpot=receiver_pool_point
    print(f'收礼人积分池 {receiver_jackpot}')


    userss=list(user.find({'_id':receiver}))
    app_info='jinquan_leader'
    if userss:
        app_info=userss[0].get('app')
    if cps and app_info=='jinquan_leader':
        print('需要验证积分池')
        jackpot_point_record = mongoUtil.connectMongo('jinquan', 'jackpot_point_record')
        jack_point=list(jackpot_point_record.find({'receiver_id':receiver}).sort([('_id', -1)]).limit(1))
        if jack_point:
            if jack_point[0].get('side') =='OUT':
                assert receiver_jackpot==0, '收礼人积分池报错'
            else:
                if time_range[0]<jack_point[0].get('create_time')<time_range[1]:
                    assert receiver_jackpot-jack_point[0].get('score')==0, '收礼人积分池报错'
                else:
                    assert receiver_jackpot==0, '收礼人积分池报错'
            print('收礼人积分池正确')
        else:
            print('收礼人积分池报错')
    else:
        print('无积分池， 不需验证')

    #删除所有积分明细
    #del_female_guest_point_record([receiver,group_leader,family_leader],delete=1)




def cal_point_0525_guanlifei(sender,receiver,real_coin=None):
    receiver_group_leader_money = 0
    sender_family_leader_money = 0
    receiver_family_leader_money = 0
    sender_group_leader_money = 0
    anchor_changdifei = 0
    changdeifei=True
    check_changdifei=False
    user_gift_record = mongoUtil.connectMongo('jinquan','user_gift_record')
    gift_record=list(user_gift_record.find({'user_id':sender,'internal_user_id':receiver}).sort([('_id',-1)]).limit(1))[0]
    gift_sender_time=gift_record.get('create_time')
    time_range=[gift_sender_time-datetime.timedelta(seconds=2),gift_sender_time+datetime.timedelta(seconds=2)]
    anchor=gift_record.get('anchor_id',None)
    if not anchor:
        anchor=gift_record.get('team_leader_id',None)
    coin=gift_record.get('price_total')
    sub_price_total=gift_record.get('sub_price_total')
    if sub_price_total and sub_price_total>coin:
        coin=sub_price_total
        changdeifei=False
    if real_coin:
        coin=real_coin
    receiver_point = coin*10*0.24
    family=mongoUtil.connectMongo('jinquan','family')

    sender_group_id,sender_family_id=get_main_family(sender)
    reveiver_group_id,reveiver_family_id=get_main_family(receiver)

    sender_group_leader_id=list(family.find({'_id':sender_group_id}))[0].get('family_head')
    sender_family_leader_id=list(family.find({'_id':sender_family_id}))[0].get('family_head')
    if sender_group_id==reveiver_group_id:
        receiver_group_leader_id= sender_group_leader_id
        receiver_family_leader_id=sender_family_leader_id
    else:
        receiver_group_leader_id= list(family.find({'_id':reveiver_group_id}))[0].get('family_head')
        receiver_family_leader_id=list(family.find({'_id':reveiver_family_id}))[0].get('family_head')

    #收礼人积分池
    receiver_pool_point=round(coin*10*0.01,2)

    female_guest_point_record=del_female_guest_point_record({receiver,sender_group_leader_id,sender_family_leader_id,receiver_group_leader_id,receiver_family_leader_id,anchor})

    groupratio=0.07
    familyratio=0.02
    sign_role_record = mongoUtil.connectMongo('jinquan', 'sign_role_record')
    slr=list(sign_role_record.find({'user_id':receiver_family_leader_id,'next_role':10}))[0]
    sign_time=slr.get('create_time')
    if sign_time<datetime.datetime.strptime('2022-07-26 11:00:00','%Y-%m-%d %H:%M:%S'):
        familyratio=0.03
        print('老家族长---')

    #家族长管理费
    receiver_family_leader_money+=coin*10*familyratio

    # 小组长管理费
    receiver_group_leader_money+=coin*10*groupratio

    #场地费
    anchor_changdifei+=coin*10*0.05

    #自己收无场地费
    if receiver==anchor or not changdeifei:
        anchor_changdifei=0
    total_group_money=None
    total_family_money=None
    if anchor == receiver_group_leader_id:
        receiver_group_leader_money+=anchor_changdifei
    elif anchor == sender_group_leader_id:
        sender_group_leader_money+=anchor_changdifei
    elif anchor ==sender_family_leader_id:
        sender_family_leader_money+=anchor_changdifei
    elif anchor == receiver_family_leader_id:
        receiver_family_leader_money+=anchor_changdifei
    else:
        if receiver!=anchor:
            check_changdifei=True

    if sender_group_id==reveiver_group_id:
        total_group_money=receiver_group_leader_money+sender_group_leader_money
        total_family_money=receiver_family_leader_money+sender_family_leader_money
    else:
        if sender_family_id == reveiver_family_id:
            total_family_money=receiver_family_leader_money+sender_family_leader_money
    if total_group_money:
        res=f'收礼人积分: {round(receiver_point,2)}\n收礼人积分池积分: {round(receiver_pool_point,2)}\n家族长总计：{round(total_family_money,2)}\n小组长总计: {round(total_group_money,2)}\n主持人场地费: {anchor_changdifei}'
    else:
        res=f'收礼人积分: {round(receiver_point,2)}\n收礼人积分池积分: {round(receiver_pool_point,2)}\n收礼人家族长总计：{round(receiver_family_leader_money,2)}\n收礼人小组长总计: {round(receiver_group_leader_money,2)}\n' \
            f'送礼人家族长总计：{round(sender_family_leader_money,2)}\n' \
            f'送礼人小组长总计: {round(sender_group_leader_money,2)}\n主持人场地费: {anchor_changdifei}'

    print(res)
    print('-'*30)

    if total_group_money:
        for i in female_guest_point_record:
            if i.get('user_id')==receiver_group_leader_id:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(total_group_money,2) ==0, f'小组长 积分报错啦！！，应得积分：{total_group_money}，实际获得：{i.get("point")}'
                    print('收礼人小组长 积分测试通过')
                else:
                    assert total_group_money==0, f'小组长积分报错啦，应得积分：{total_group_money}，实际获得：0'
            elif i.get('user_id')==receiver_family_leader_id:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(total_family_money,2) ==0, f'家族长 积分报错啦！！ ，应得积分：{total_family_money}，实际获得：{i.get("point")}'
                    print('收礼人家族长 积分测试通过')
                else:
                    assert total_group_money==0, f'家族长积分报错啦, ，应得积分：{total_family_money}，实际获得：0'
            elif i.get('user_id')==receiver:
                assert i.get('point') - round(receiver_point,2) ==0, '收礼人 积分报错啦！！'
                print('收礼人 积分测试通过')
            elif check_changdifei and i.get('user_id')==anchor:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(anchor_changdifei,2) ==0, f'主持人场地费 积分报错啦！！，应得积分：{anchor_changdifei}，实际获得：{i.get("point")}'
                    print('主持人场地费 积分测试通过')
                else:
                    assert round(anchor_changdifei,2)==0, f'主持人场地费 积分报错啦，应得积分：{round(anchor_changdifei,2)}，实际获得：0'
    else:
        for i in female_guest_point_record:
            if i.get('user_id')==receiver_group_leader_id:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(receiver_group_leader_money,2) ==0, f'收礼人小组长 积分报错啦！！，应得积分：{receiver_group_leader_money}，实际获得：{i.get("point")}'
                    print('收礼人小组长 积分测试通过')
                else:
                    assert receiver_group_leader_money==0,f'收礼人小组长 积分报错啦！！，应得积分：{receiver_group_leader_money}，实际获得：0'
                    print('收礼人小组长 积分测试通过')
            elif i.get('user_id')==sender_group_leader_id:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(sender_group_leader_money,2) ==0, f'送礼人小组长 积分报错啦！！，应得积分：{sender_group_leader_money}，实际获得：{i.get("point")}'
                    print('送礼人小组长  积分测试通过')
                else:
                    assert sender_group_leader_money==0,f'送礼人小组长 积分报错啦！！，应得积分：{receiver_group_leader_money}，实际获得：0'
                    print('送礼人小组长，积分测试通过')
            elif i.get('user_id')==receiver_family_leader_id:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(receiver_family_leader_money,2) ==0, f'收礼人家族长 积分报错啦！！，应得积分：{receiver_family_leader_money}，实际获得：{i.get("point")}'
                    print('收礼人家族长  积分测试通过')
                else:
                    assert receiver_family_leader_money==0, f'收礼人家族长 积分报错啦！！，应得积分：{receiver_family_leader_money}，实际获得：0'
                    print('收礼人家族长  积分测试通过')
            elif i.get('user_id')==sender_family_leader_id:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(sender_family_leader_money,2) ==0, f'送礼人家族长 积分报错啦！！，应得积分：{sender_family_leader_money}，实际获得：{i.get("point")}'
                    print('送礼人家族长 积分测试通过')
                else:
                    assert sender_family_leader_money==0, f'送礼人家族长 积分报错啦！！，应得积分：{sender_family_leader_money}，实际获得：0'
                    print('送礼人家族长  积分测试通过')
            elif i.get('user_id')==receiver:
                assert i.get('point') - round(receiver_point,2) ==0, '收礼人 积分报错啦！！'
                print('收礼人 积分测试通过')
            elif check_changdifei and i.get('user_id')==anchor:
                if time_range[0]<datetime.datetime.strptime(i.get('create_time'),'%Y-%m-%d %H:%M:%S')<time_range[1]:
                    assert i.get('point') - round(anchor_changdifei,2) ==0, f'主持人场地费 积分报错啦！！，应得积分：{anchor_changdifei}，实际获得：{i.get("point")}'
                    print('主持人场地费 积分测试通过')
                else:
                    assert round(anchor_changdifei,2)==0, f'主持人场地费 积分报错啦，应得积分：{round(anchor_changdifei,2)}，实际获得：0'

    #积分池
    receiver_jackpot=round(coin*10*0.01,2)
    couple_relation_unique=mongoUtil.connectMongo('jinquan','couple_relation_unique')
    cps=list(couple_relation_unique.find({'$or':[{'user_id':sender,'bind_user_id':receiver,'deleted':0},{'user_id':receiver,'bind_user_id':sender,'deleted':0}]}))
    user=mongoUtil.connectMongo('jinquan','user')
    userss=list(user.find({'_id':receiver}))
    app_info='jinquan_leader'
    if userss:
        app_info=userss[0].get('app')
    if cps and app_info=='jinquan_leader':
        print('需要验证积分池')
        jackpot_point_record = mongoUtil.connectMongo('jinquan', 'jackpot_point_record')
        jack_point=list(jackpot_point_record.find({'receiver_id':receiver}).sort([('_id', -1)]).limit(1))
        if jack_point:
            assert receiver_jackpot-jack_point[0].get('score')==0, f'收礼人积分池报错，应得{receiver_jackpot}，实际获得{jack_point[0].get("score")}'
            print('收礼人积分池正确')
        else:
            print('收礼人积分池报错')
    else:
        print('无积分池， 不需验证')

if __name__ == '__main__':
    user_info={'qingwa':'1867291051','water':'1787542671','ge': '1772113311','cat':'1452460951',
               'moon':'1480845661','c3c':'1733610301'}

    #cal_point(100,receiver=user_info.get('water'),anchor=cat,glSingle=False)
    #del_female_guest_point_record([duoilamisao1,moon,cat],delete=1),glSingle=False
    sender=user_info.get('qingwa')
    receiver=user_info.get('water') #,anchor=user_info.get('cat')
    cal_point(sender,receiver,scene='family')
    # cal_point_0525_guanlifei(sender,receiver)
