
from 测试脚本.personal.mongconnect import mongoUtil

mongoUtil = mongoUtil()

class UserAccount:
    user_account=mongoUtil.connectMongo('account','user_account')
    def get_user_account(self,id):
        res=self.user_account.find_one({'_id':id})
        return res

    def get_user(self,id):
        user = mongoUtil.connectMongo('jinquan', 'user')
        return user.find_one({'_id':id})


if __name__ == '__main__':
    userAcc=UserAccount()

    acc=userAcc.get_user_account('1452460951')
    print(acc)

    usera=userAcc.get_user('1452460951')
    print(usera)
    print(acc.keys())

