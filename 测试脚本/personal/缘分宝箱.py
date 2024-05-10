import json
import time

import requests

from 测试脚本.personal.common import Common_Function
from 测试脚本.personal.redisUtil import RedisUtil
from 测试脚本.personal.mongconnect import mongoUtil
from 测试脚本.personal.常規 import del_friend_relation
mongoUtil = mongoUtil()

redis_db1 = RedisUtil().connect_redis()


class fate_box(Common_Function):

    # 更新数据库
    def update_fate_box(self, uid,state=2):
        fate_box = mongoUtil.connectMongo('jinquan', 'fate_box')
        fate_box_result = fate_box.update_many({'user_id': uid}, {'$set': {'state': state}})
        if fate_box_result.modified_count != 1:
            print('fate_box 数据修改失败！')
        redis_key_fate_box = f'fate_box:{uid}'
        redis_db1.delete(redis_key_fate_box)
        res = fate_box.find_one({'user_id': uid})
        return str(res.get('_id'))

    def query_gift_id(self, uid):
        fate_box = mongoUtil.connectMongo('jinquan', 'fate_box')
        res = fate_box.find_one({'user_id': uid})
        return str(res.get('gift_id'))

    def query_fate_box(self, uid):
        fate_box = mongoUtil.connectMongo('jinquan', 'fate_box')
        res = fate_box.find({'user_id': uid}).sort([('_id', -1)])
        for i in res:
            print(i)
    def open_fate_box(self, uid, num=1):
        url = 'http://advanced-poros.test.diffusenetwork.net/service/user/open_fate_box_test'
        result = {}
        for i in range(num):
            fate_box_id = self.update_fate_box(uid)
            params = {
                "room_id": "15550469473",
                "pos": "1",
                "fate_box_id": fate_box_id,
                "token": self.get_token(uid)
            }
            res = requests.request(method='POST', url=url, data=json.dumps(params))
            time.sleep(5)
            print(res.json())
            if res.json()['code'] == 0:
                gift_id=res.json()['data']['fate_gift_id']
                if gift_id in result.keys():
                    result[gift_id] = result[gift_id] + 1
                else:
                    result[gift_id] = 1
        return result

    def del_relation(self,uid):
        user_relation=mongoUtil.connectMongo('jinquan','user_relation')
        res=user_relation.delete_many({'c_user_id':uid})
        print(f'关系删除{res.deleted_count}')

    def del_fate_box(self,uid,buid=''):
        fate_box = mongoUtil.connectMongo('jinquan', 'fate_box')
        fate_box_result = fate_box.delete_many({'user_id': uid})
        print(f'删除宝箱{fate_box_result.deleted_count}')
        redis_key_fate_box = f'fate_box:{uid}'
        redis_db1.delete(redis_key_fate_box)
        self.del_relation(uid)
        del_friend_relation(uid)
        # redis_friend_relation=f'video_room:friend:{uid}:{buid}'
        # redis_db1.delete(redis_friend_relation)
if __name__ == '__main__':
    cuid='1585526341'
    #moon 1480845661
    buid_list=['1480845661','1580635371']
    fate_box=fate_box()
    url='http://advanced-poros.test.diffusenetwork.net/ccc/fate_box/info?fate_box_id=661506184732ce983db9c83e&token=43499641-22c9-4731-a83a-c09764091062'
    res=requests.request(method='get',url=url)
    print(res.json())