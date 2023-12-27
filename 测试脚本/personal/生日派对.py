import datetime

from 测试脚本.personal.common import Common_Function
from 测试脚本.personal.mongconnect import mongoUtil

mongo = mongoUtil()


class Birthday_Party(Common_Function):

    #获取开启生日派对权限
    def get_permission(self, uid):
        data_birthday_party_user = mongo.connectMongo(0, 'jinquan', 'data_birthday_party_user')
        # .strftime('%Y-%m-%d')
        print(datetime.datetime.now())
        yesterday = (datetime.datetime.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)).strftime('%Y-%m-%d')
        print(yesterday)
        document = {'user_id': uid, 'dt': yesterday}
        print(document)
        data_birthday_party_user.insert_one(document)


if __name__ == '__main__':
    birthday_party = Birthday_Party()
    birthday_party.get_permission('1464011321')
