from 测试脚本.personal.mongconnect import mongoUtil

mongo = mongoUtil()

user_gift_wall=mongo.connectMongo('all_database','user_gift_wall',db='gift')

user_gift_record=mongo.connectMongo('jinquan','user_gift_record')

for i in user_gift_record.find():
    print(i)

res=user_gift_wall.find()

for i in res:
    print(i)