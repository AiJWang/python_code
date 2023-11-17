import datetime

from bson import ObjectId

from 测试脚本.personal.mongconnect import mongoUtil

mongoUtil=mongoUtil()

database='couple'



def get_romanticlist_point_reward(query):
    romanticlist_point_detail = mongoUtil.connectMongo(2, database, 'romanticlist_point_detail')

    now=datetime.datetime.now()
    update={'$set':{'create_time':now,'update_time':now}}
    result=romanticlist_point_detail.update_many(query,update)
    print(result)



if __name__=='__main__':
    query={'_id':ObjectId('654ca3d87506000073000ff3')}
    get_romanticlist_point_reward(query)