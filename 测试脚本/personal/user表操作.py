
import datetime

from 测试脚本.personal.mongconnect import mongoUtil

mongoUtil=mongoUtil()
user = mongoUtil.connectMongo('jinquan', 'user')


def update_user_info():
    #user.update_one({'_id':'1430449181'},{'$set':{'return_time':'1701164195000'}})
    res=user.find({'_id':'1430449181'})

    for i in res:
        print(i)

def delete_user():
    user.delete_many({'real_name':'王爱军'})


if __name__=='__main__':
    delete_user()