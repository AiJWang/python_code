import random

import pymongo,redis
from datetime import datetime
from pymongo import  DESCENDING


class My_Mongodb:
    def __init__(self, url, db):
        self.client = pymongo.MongoClient(url)
        self.mydb = self.client[db]
        self.mytab = None
    def connect_table(self, table):
        self.mytab = self.mydb[table]
        return self.mytab
    def query_data(self, **kwargs):
        myquery = kwargs
        return self.mytab.find_one(myquery)

    def query_alldata(self, **kwargs):
        myquery = kwargs
        return self.mytab.find(myquery)

    def insert_data(self, kwargs):
        self.mytab.insert_one(kwargs)

    def update_data(self, set_dict, **find_dict):
        self.mytab.update_one(find_dict, {'$set': set_dict})

    def update_alldata(self, set_dict, **find_dict):
        self.mytab.update_many(find_dict, {'$set': set_dict})

class My_Redis:
    def __init__(self, host, port, passwd, db):
        self.r = redis.Redis(host=host, port=int(port), password=passwd, db=int(db))

    def get_data(self, key, start, end):
        return self.r.zrange(key, start, end)

    def get_rdata(self, key):
        return self.r.get(key)

    def get_hash_data(self,key):
        return self.r.hgetall(key)

    def set_rdata(self, key, value):
        return self.r.set(key, value)

    def set_hash_data(self,my_hash, field, value):
        return self.r.hset(my_hash, field, value)

    def update_rdata(self, key, value, score):
        self.r.zadd(key, {value:score})

    def delete_data(self, key):
        self.r.delete(key)

class Group:
    def __init__(self):
        self.r = My_Redis("r-2zer3tg1gl0ao7wssspd.redis.rds.aliyuncs.com", "6379", "lFofuO80V0", "1")
        self.f = My_Mongodb("mongodb://poros_test:6nKBKbCdBxizNRQJ@s-2ze804aac801b914-pub.mongodb.rds.aliyuncs.com:3717/jinquan","jinquan")
        self.time_str = "2021-07-22 20:50:02"
        self.format_str = "%Y-%m-%d %H:%M:%S"
        self.time_dt = datetime.strptime(self.time_str, self.format_str)
    def group(self,userid,group):
        """- 'CONTROL' 对照组
                - 'A' 实验组A   #实验组A已经不存在了
                - 'B' 实验组B
                - 'C' 实验组C   #实验组C已经不存在了
                - 'D' 实验组D"""
        if group == "D":
            self.f.connect_table("user")
            self.f.update_data({"register_time":"1663851002000"},_id=str(userid))
            self.f.connect_table("user_device")
            create_time=f'2022-09-01 {random.randrange(10,50)}:{random.randrange(10,50)}:{random.randrange(10,50)}'
            self.f.update_alldata({"create_time":create_time,"device_id":"c3Em4XNVRGiM6VbZ51Un"},user_id=str(userid))

        elif group == "CONTROL":
            self.f.connect_table("user")
            self.f.update_data({"register_time":"1658494202000"},_id=str(userid))

        elif group == "old_leader":

            self.f.connect_table("sign_role_record")
            self.f.update_data({"create_time": self.time_dt}, user_id=str(userid), next_role=6)
            self.r.delete_data(f"user:sign_role:first:ts:{userid}:6")

        elif group == "old_room":

            self.f.connect_table("sign_role_record")
            self.f.update_data({"create_time": self.time_dt}, user_id=str(userid), next_role=4)
            self.r.delete_data(f"user:sign_role:first:ts:{userid}:4")

        elif group == "old_5_room":

            self.f.connect_table("sign_role_record")
            self.f.update_alldata({"create_time": self.time_dt}, user_id=str(userid), next_role=8)
            self.r.delete_data(f"user:sign_role:first:ts:{userid}:8")

        elif group == "old_group_leader":
            self.f.connect_table("sign_role_record")
            self.f.update_alldata({"create_time":self.time_dt},user_id=str(userid),next_role=9)
            self.r.delete_data(f"user:sign_role:first:ts:{userid}:9")

        elif group == "old_family":
            self.f.connect_table("sign_role_record")
            self.f.update_alldata({"create_time":self.time_dt},user_id=str(userid),next_role=10)
            self.r.delete_data(f"user:sign_role:first:ts:{userid}:10")

        print("修改成功")

if __name__ == '__main__':
    f = Group()
    user_info={'qingwa':'1688205221','water':'1726058281','maoer':'1604497831','nier':'1604468611','huoxing':'1642724051'}
    userid=user_info.get('huoxing')
    group = "old_leader"  # 修改账号时，第一次执行group值选择CONTROL或者D执行一次，然后同一个id执行group值选择old_group_leader或者old_family或者old_room或者old_leader或者old_5_room中的任意一个，执行第二次

    # CONTROL，修改2022年7月26日以前注册的B端签约领队身份的用户积分分成。
    # D，修改2022年7月26日至2022年10月20日11点之前注册的B端签约领队身份的用户的积分分成

    # old_group_leader，修改小组长的管理费和任务KPI。
    # old_family，修改家族长的管理费和任务KPI。
    # old_room，修改语音房主持人的管理费和任务KPI。
    # old_leader，成为签约领队时间，修改签约领队的管理费和任务KPI。
    # old_5_room，成为签约领队时间，修改五人房主持人的管理费和任务KPI
    f.group(userid,'CONTROL')
    #f.group(userid,'old_leader')


