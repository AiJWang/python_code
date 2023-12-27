from 测试脚本.personal.mongconnect import mongoUtil

class Common_Function:
    mongo = mongoUtil()

    #获取token
    def get_token(self,uid):
        if not uid:
            return None
        user_session = self.mongo.connectMongo(0, 'jinquan', 'user_session')
        res = user_session.find_one({'user_id': uid, 'deleted': 0})
        return res['session_id']