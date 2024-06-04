import datetime

import pytest
import requests

from 测试脚本.personal.common import Common_Function
from 测试脚本.personal.女嘉宾积分相关 import del_signed_voice_female_monthly
from 测试脚本.personal.常規 import del_female_guest_point_record, update_interactive_value
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
def cal_point(coin,sender,receiver,anchor=None,scene='room'):
    receiver_group_leader_money = 0
    sender_family_leader_money = 0
    receiver_family_leader_money = 0
    sender_group_leader_money = 0
    anchor_changdifei = 0

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
    familyratio=0.01
    if scene=='family':
        groupratio=0.035
    elif scene== 'chat':
        groupratio=0
        familyratio=0
    else:
        groupratio=0.017

    #家族长管理费
    receiver_family_leader_money+=coin*10*familyratio
    sender_family_leader_money+=coin*10*familyratio

    # 小组长管理费
    receiver_group_leader_money+=coin*10*groupratio
    sender_group_leader_money+=coin*10*groupratio

    #场地费
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
                assert i.get('point') - round(total_group_money,2) ==0, '小组长 积分报错啦！！'
                print('收礼人小组长 积分测试通过')
            elif i.get('user_id')==receiver_family_leader_id:
                assert i.get('point') - round(total_family_money,2) ==0, '家族长 积分报错啦！！'
                print('收礼人家族长 积分测试通过')
            elif i.get('user_id')==receiver:
                assert i.get('point') - round(receiver_point,2) ==0, '收礼人 积分报错啦！！'
                print('收礼人 积分测试通过')
    else:
        for i in female_guest_point_record:
            if i.get('user_id')==receiver_group_leader_id:
                assert i.get('point') - round(receiver_group_leader_money,2) ==0, '收礼人小组长 积分报错啦！！'
                print('收礼人小组长 积分测试通过')
            elif i.get('user_id')==sender_group_leader_id:
                assert i.get('point') - round(sender_group_leader_money,2) ==0, '送礼人小组长 积分报错啦！！'
                print('送礼人小组长  积分测试通过')
            elif i.get('user_id')==receiver_family_leader_id:
                assert i.get('point') - round(receiver_family_leader_money,2) ==0, '收礼人家族长 积分报错啦！！'
                print('收礼人家族长  积分测试通过')
            elif i.get('user_id')==sender_family_leader_id:
                assert i.get('point') - round(sender_family_leader_money,2) ==0, '送礼人家族长 积分报错啦！！'
                print('送礼人家族长 积分测试通过')
            elif i.get('user_id')==receiver:
                assert i.get('point') - round(receiver_point,2) ==0, '收礼人 积分报错啦！！'
                print('收礼人 积分测试通过')

    #积分池
    receiver_jackpot=round(coin*10*0.01,2)
    print(f'收礼人积分池 {receiver_jackpot}')
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
            assert receiver_jackpot-jack_point[0].get('score')==0, '收礼人积分池报错'
            print('收礼人积分池正确')
        else:
            print('收礼人积分池报错')
    else:
        print('无积分池， 不需验证')

    #删除所有积分明细
    #del_female_guest_point_record([receiver,group_leader,family_leader],delete=1)




def cal_point_0525_guanlifei(sender,receiver):
    receiver_group_leader_money = 0
    sender_family_leader_money = 0
    receiver_family_leader_money = 0
    sender_group_leader_money = 0
    anchor_changdifei = 0

    user_gift_record = mongoUtil.connectMongo('jinquan','user_gift_record')
    gift_record=list(user_gift_record.find({'user_id':sender,'internal_user_id':receiver}).sort([('_id',-1)]).limit(1))[0]
    gift_sender_time=gift_record.get('create_time')
    time_range=[gift_sender_time-datetime.timedelta(seconds=2),gift_sender_time+datetime.timedelta(seconds=2)]
    anchor=gift_record.get('anchor_id',None)
    if not anchor:
        anchor=gift_record.get('team_leader_id',None)
    coin=gift_record.get('price_total')

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


    #家族长管理费
    receiver_family_leader_money+=coin*10*familyratio

    # 小组长管理费
    receiver_group_leader_money+=coin*10*groupratio

    #场地费
    anchor_changdifei+=coin*10*0.05

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

    #删除所有积分明细
    #del_female_guest_point_record([receiver,group_leader,family_leader],delete=1)

if __name__ == '__main__':
    user_info={'qingwa':'1688205221','water':'1726058281','maoer':'1604497831','nier':'1604468611','cat':'1452460951',
               'moon':'1480845661','sunflower':'1604589981','iq':'1622722681','huoxing':'1642724051','ge': '1600740271',
               'c3c':'1733610301','sun':'1734748351','qu':'1687572931'}

    #cal_point(100,receiver=user_info.get('water'),anchor=cat,glSingle=False)
    #del_female_guest_point_record([duoilamisao1,moon,cat],delete=1),glSingle=False
    sender=user_info.get('qu')
    receiver=user_info.get('huoxing')
    cal_point_0525_guanlifei(sender,receiver)
