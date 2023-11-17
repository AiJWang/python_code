import datetime
import random

import pymongo
from bson import ObjectId
from pymongo import MongoClient
import json


# 链接数据库
class mongoUtil:
    __mongoUrlList = (
        'mongodb://poros_test:6nKBKbCdBxizNRQJ@s-2ze804aac801b914-pub.mongodb.rds.aliyuncs.com:3717/jinquan',
        'mongodb://ugc:aUWjzhRkIk@s-2ze804aac801b914-pub.mongodb.rds.aliyuncs.com:3717,s-2zeaffa80a551f74-pub.mongodb.rds.aliyuncs.com:3717/ugc',
        'mongodb://couple_service:aUWjzhRkIk@s-2ze804aac801b914-pub.mongodb.rds.aliyuncs.com:3717/?retryReads=false&retryWrites=false&authSource=couple')

    def connectMongo(self, urlIndex, db, table):
        print(self.__mongoUrlList[urlIndex])
        return MongoClient(self.__mongoUrlList[urlIndex])[db][table]


    def querytest08(self):
        collection = self.connectMongo(0, 'jinquan', 'user')
        query = {'_id': '1208761381'}
        for i in collection.find(query):
            print(i)
        # 修改注册时的婚姻状态
        # update={'$set':{'marital_stat':0}}
        # x=collection.update_one(query,update)
        # print(x)
        # print(collection.find_one(query))
        # jsonstr=json.dumps(i)
        # print(jsonstr)

    def queryData(self, collection, query):
        result = collection.find(query)
        return result

    def insertData(self, collection, data):
        collection.insert_one(data)

    def test1(self):
        cc=self.connectMongo(2,'couple','romanticlist_point_reward')
        res=cc.find({'male_user_id':'1413125201'})
        for i in res:
            print(i)
        # mc = self.connectMongo1('s-2ze804aac801b914-pub.mongodb.rds.aliyuncs.com',
        #                                                   'couple_service', '748BAC673E36E177126AD3018D3A9963',
        #                                                   'couple')
        # mc=pymongo.MongoClient('mongodb://couple_service@s-2ze804aac801b914-pub.mongodb.rds.aliyuncs.com:3717/').couple.authenticate("couple_service","748BAC673E36E177126AD3018D3A9963")
        # mc = pymongo.MongoClient(
        #     host='mongodb://couple_service@s-2ze804aac801b914-pub.mongodb.rds.aliyuncs.com', port=3717,
        #     username='couple_service',
        #     # 密码
        #     password='748BAC673E36E177126AD3018D3A9963',
        #     # 需要用户名和密码进行身份认证的数据库
        #     authSource='couple')
        # db=mc.couple
        # # mc.list_database_names()
        # # print(mc.list_database_names())
        # get_romanticlist_point_reward = db['get_romanticlist_point_reward']
        # res = get_romanticlist_point_reward.find()
        # for i in res:
        #     print(i)


    def test(self):
        mongoUtil1 = mongoUtil()
        taiyang = {'userid': '1074590021', 'unionid': '615015c215703a6fd28e39d4', 'familyid': '50597939'}
        diaochan = {'userid': '1266430511', 'unionid': '615015c215703a6fd28e39d4', 'familyid': '97895279'}
        wdiaochan = {'userid': '1256780371', 'unionid': '615015c215703a6fd28e39d4', 'familyid': '97895279'}

        mx_comment = mongoUtil1.connectMongo(1, 'ugc', 'mx_comment')
        query = {'_id': ObjectId('6527b71a27a0a690e2da4753')}
        result = mongoUtil1.queryData(mx_comment, query)
        data = dict(result[0])
        data.pop('_id')
        # data.pop('create_time')
        # data.pop('update_time')
        # data['family_id'] = taiyang['familyid']
        # data['group_leader_id'] = taiyang['userid']
        # data['union_id'] = taiyang['unionid']
        # data['comment'] = 'good girl'
        print(data)
        ss = mongoUtil1.insertData(mx_comment, data)
        print(ss)


if __name__ == '__main__':
    mm = mongoUtil()

    mm.test1()
