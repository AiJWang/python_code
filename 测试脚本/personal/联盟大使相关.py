from bson import ObjectId

from 测试脚本.personal.mongconnect import mongoUtil

mongo = mongoUtil()


#库改了，应该不是这个库了

class UnionABD:

    # 团队邀请码
    def team_invite_code(self):
        team_invite_code = mongo.connectMongo(0, 'jinquan', 'team_invite_code')
        res = team_invite_code.find().limit(10)
        for i in res:
            print(i)

    # 个人邀请码
    def user_invitation_code_v2(self,uid):
        user_invitation_code_v2 = mongo.connectMongo(0, 'jinquan', 'user_invitation_code_v2')
        res = user_invitation_code_v2.find({'_id':uid}).limit(10)
        for i in res:
            print(i)

if __name__ == '__main__':
    abd = UnionABD()
    abd.user_invitation_code_v2('1452460951')
