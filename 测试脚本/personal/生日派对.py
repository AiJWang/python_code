import datetime

from bson import ObjectId

from 测试脚本.personal.common import Common_Function
from 测试脚本.personal.mongconnect import mongoUtil
from 测试脚本.personal.redisUtil import RedisUtil

mongo = mongoUtil()
redis_db1=RedisUtil().connect_redis()


class Birthday_Party(Common_Function):

    #获取开启生日派对权限
    def get_permission(self, uid):
        data_birthday_party_user = mongo.connectMongo('jinquan', 'data_birthday_party_user')
        # .strftime('%Y-%m-%d')
        print(datetime.datetime.now())
        yesterday = (datetime.datetime.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)).strftime('%Y-%m-%d')
        print(yesterday)
        document = {'user_id': uid, 'dt': yesterday}
        print(document)
        data_birthday_party_user.insert_one(document)

    def insert_intimacy_users(self,uid,intimacy_array):
        data_birthday_party_user_intimacy_list = mongo.connectMongo('jinquan', 'data_birthday_party_user_intimacy_list')
        #result=data_birthday_party_user_intimacy_list.find().limit(10)
        data={'user_id': uid, 'birth': '2024-02-28',
              'union_id': '615015c215703a6fd28e39d4', 'intimacy_array':intimacy_array, 'app': 'jinquan', 'biz': 'jinquan'}
        resu=data_birthday_party_user_intimacy_list.insert_one(data)
        print(resu.inserted_id)

    def del_birthday_party_remind(self,uid):
        birthday_party_remind= mongo.connectMongo('jinquan', 'birthday_party_remind')
        res=birthday_party_remind.delete_one({'_id':ObjectId('65dede30eef673ec484b18ae')})
        print(res.deleted_count)

    def del_redis_data(self,uid):
        update_birth=f'ac-birth-update-count:{uid}'
        sned_card_redis=f'SendRemindMsgKey:2024-03-01:{uid}'
        redis_db1.delete(update_birth)
        redis_db1.delete()


if __name__ == '__main__':
    birthday_party = Birthday_Party()
    womendequ='1538701411'
    womendege='1548780921'
    cat = '1452460951'
    shuixing='1508726511'
    #birthday_party.insert_intimacy_users(cat,[womendequ,womendege])
    #birthday_party.del_birthday_party_remind(cat)
    birthday_party.insert_intimacy_users('1090140181',['999781791'])
