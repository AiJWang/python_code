import datetime

from 测试脚本.personal.mongconnect import mongoUtil

mongoUtil=mongoUtil()

def updateTime(dict):
    couple_level_relation = mongoUtil.connectMongo(0, 'jinquan', 'couple_level_relation')
    #修改组cp的时间
    couple_level_relation.update_one(dict,{'$set':{'finish_time':datetime.datetime(2023, 10, 31, 19, 31, 21, 943000)}})
    res=couple_level_relation.find(dict)

    for i in res:
        print(i)

def updateRegisterVersion(dict):
    user = mongoUtil.connectMongo(0, 'jinquan', 'user')
    #修改注册版本 版本大于1.9.9.3的 并且user_id 还得大于 xxx 算是新用户
    user.update_one(dict,{'$set':{'register_version':'2.0.3.3'}})
    res=user.find(dict)
    for i in res:
        print(i)

if __name__=='__main__':
    #updateTime({'male_user_id':'1412634311'})
    print(131197922781>294845150321)