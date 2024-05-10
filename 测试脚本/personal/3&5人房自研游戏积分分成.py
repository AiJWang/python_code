import pytest
from 测试脚本.personal.女嘉宾积分相关 import del_signed_voice_female_monthly
from 测试脚本.personal.常規 import del_female_guest_point_record
from 测试脚本.personal.mongconnect import mongoUtil


mongoUtil = mongoUtil()
cat ='1452460951'
water ='1508726511'
moon ='1480845661'

huoxing_Bman='1549993261'


womendege ='1538701411'
womendequ = '1550164531'

sun='1549825981'

iqoo_c_girl='1549980551'

# flDouble 家族长双份     glSingle： 小组长单分
def cal_point(coin,receiver=cat,group_leader=cat,family_leader=moon,anchor=moon,changdifei=True,flDouble=True,glSingle=True):
    family_leader_point = 0
    group_leader_point = 0
    anchor_changdifei = 0
    user = mongoUtil.connectMongo('jinquan', 'user')
    #receiver_info=user.find({'_id':receiver})[0]
    #判断男女
    # if receiver_info.get('gender')==2:
    #     receiver_point = coin*10*0.15
    # else:
    #     receiver_point = coin*10*0.1
    receiver_point = coin*10*0.15
    if receiver =='1508726511':
        receiver_point = coin * 10 * 0.1

    receiver_pool_point=coin*10*0.05
    female_guest_point_record=del_female_guest_point_record({receiver,group_leader,family_leader,anchor})
    #家族长管理费
    if flDouble:
        family_leader_point+=coin*10*0.02

    # 小组长管理费
    if glSingle:
        group_leader_point+=coin*10*0.017
    else:
        group_leader_point += coin * 10 * 0.034
    #场地费
    if changdifei:
        anchor_changdifei+=coin*10*0.1
    #自己收无场地费
    if receiver==anchor:
        anchor_changdifei=0

    if anchor==family_leader:
        family_leader_point+=anchor_changdifei
    if anchor==group_leader:
        group_leader_point+=anchor_changdifei
    if receiver==group_leader:
        receiver_point+=group_leader_point
    if receiver==family_leader:
        receiver_point+=family_leader_point

    res=f'''收礼人积分: {receiver_point}
收礼人积分池积分: {receiver_pool_point}
家族长总计：{family_leader_point}
小组长总计: {round(group_leader_point,2)}
主持人场地费: {anchor_changdifei}'''

    print(res)
    print('-'*30)

    for i in female_guest_point_record:
        if receiver == group_leader :
            if i.get('user_id')==group_leader:
                assert i.get('point') - receiver_point ==0, '收礼人小组长 小组长 积分报错啦！！'
                print('收礼人小组长 小组长 积分测试通过')
            elif i.get('user_id')==family_leader:
                assert i.get('point') - family_leader_point ==0, '收礼人小组长  家族长 积分报错啦！！'
                print('收礼人小组长  家族长 积分测试通过')

        elif receiver == family_leader :
            if i.get('user_id')==family_leader:
                assert i.get('point') - receiver_point ==0, '收礼人家族长 家族长 积分报错啦！！'
                print('收礼人家族长 家族长 积分测试通过')
            elif i.get('user_id')==group_leader:
                assert i.get('point') -  round(group_leader_point,2) ==0, '收礼人家族长 小组长 积分报错啦！！'
                print('收礼人家族长 小组长 积分测试通过')
        else:
            if i.get('user_id')==family_leader:
                assert i.get('point') - family_leader_point ==0, '家族长 积分报错啦！！'
                print('家族长 积分测试通过')
            elif i.get('user_id')==group_leader:
                assert i.get('point') - round(group_leader_point,2) ==0, '小组长 积分报错啦！！'
                print('小族长 积分测试通过')
            elif i.get('user_id') == receiver:
                assert i.get('point') - receiver_point ==0, '收礼人 积分报错啦！！'
                print('收礼人 积分测试通过')

    #积分池
    receiver_jackpot=coin*10*0.05
    jackpot_point_record = mongoUtil.connectMongo('jinquan', 'jackpot_point_record')
    jack_point=list(jackpot_point_record.find({'receiver_id':receiver}).sort([('_id', -1)]).limit(1))
    if jack_point and len(jack_point)>0:
        assert receiver_jackpot-jack_point[0].get('score')==0, '收礼人积分池报错'
        print('收礼人积分池正确')
    else:
        # if receiver_info.get('is_leader_client')=='true':
        #     assert False ,'收礼人无积分池'
        # else:
        #     print('非b端用户，无积分池')
        pass

    #删除所有积分明细
    #del_female_guest_point_record([receiver,group_leader,family_leader],delete=1)


if __name__ == '__main__':
    cal_point(99,receiver=cat,anchor=moon)
    #del_female_guest_point_record([duoilamisao1,moon,cat],delete=1),glSingle=False
