from 测试脚本.personal.mongconnect import mongoUtil

class Common_Function:
    mongo = mongoUtil()

    #获取token
    def get_token(self,uid):
        if not uid:
            return None
        user_session = self.mongo.connectMongo('jinquan', 'user_session')
        res = user_session.find_one({'user_id': uid, 'deleted': 0})
        return res['session_id']

    def get_money(self,uid):
        if not uid:
            return None
        user_account= self.mongo.connectMongo('account', 'user_account')
        res=user_account.update_many({'_id':uid},{'$set':{'coin':100000,'freecoin':0,'giftcoin':100000}})

        return res.modified_count