import requests

from 测试脚本.personal.mongconnect import mongoUtil

mongoUtil=mongoUtil()

#修改恩爱值
def update_love_socre(male_user_id,inter_user_id,love_score=299):
    couple_relation = mongoUtil.connectMongo(0, 'jinquan', 'couple_relation')
    query={'male_user_id':male_user_id,'internal_user_id':inter_user_id}
    ress=couple_relation.find(query)
    for i in ress:
        print(i)
    value={'$set':{'love_score':love_score}}
    res=couple_relation.update_many(query,value)

    print(res)

#修改互动值
def update_interactive_value(male_user_id,inter_user_id,value=30):
    couple_relation = mongoUtil.connectMongo(0, 'jinquan', 'couple_relation')
    query={'male_user_id':male_user_id,'internal_user_id':inter_user_id}
    ress=couple_relation.find(query)
    for i in ress:
        print(i)
    value={'$set':{'interactive_value':value}}
    res=couple_relation.update_many(query,value)

    print(res)

#修改cp陪伴礼物   盲盒
def update_blind_box(cuid,buid,num=0):
    c_p_blind_box = mongoUtil.connectMongo(0, 'jinquan', 'c_p_blind_box')
    if cuid>buid:
        cp_tag =buid+"_"+cuid
    else:
        cp_tag=cuid+"_"+buid
    query={'cp_tag':cp_tag}
    print(query)
    c_p_blind_box.update_many(query,{'$set':{'cnt':num}})

#修改金虎数量
def update_golden_tigers(uid,num=0):
    user_attach = mongoUtil.connectMongo(0, 'jinquan', 'user_attach')
    user_attach.update_many({'_id':uid},{'$set':{'golden_tigers':num}})


#判断房间类型

def room_type(familyid):
    family = mongoUtil.connectMongo(0, 'jinquan', 'family')


if __name__=='__main__':
    update_golden_tigers('1464011321',1)

