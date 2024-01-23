import datetime

from bson import ObjectId

from 测试脚本.personal.mongconnect import mongoUtil
from 测试脚本.personal.redisUtil import RedisUtil

mongo = mongoUtil()
jinquan_redis=RedisUtil().connect_redis()

#库改了，应该不是这个库了

class UnionABD:

    # 团队邀请码
    def team_invite_code(self):
        team_invite_code = mongo.connectMongo('jinquan', 'team_invite_code')
        res = team_invite_code.find().limit(10)
        for i in res:
            print(i)

    # 个人邀请码
    def user_invitation_code_v2(self,uid):
        user_invitation_code_v2 = mongo.connectMongo('jinquan', 'user_invitation_code_v2')
        res = user_invitation_code_v2.find({'_id':uid}).limit(10)
        for i in res:
            print(i)

    #额外奖励记录 被邀请人送礼物获得的额外积分
    def union_abd_extra_record(self,union_abd_id):
        union_abd_extra_record = mongo.connectMongo('jinquan', 'union_abd_extra_record')
        res = union_abd_extra_record.find({'union_abd_id':union_abd_id})
        for i in res:
            print(i)

    #奖励记录 被邀请人绑定邀请码，组cp等积分
    def union_abd_point_record(self,union_abd_id):
        union_abd_point_record = mongo.connectMongo('jinquan', 'union_abd_point_record')
        res = union_abd_point_record.find({'union_abd_id':union_abd_id})
        for i in res:
            print(i)

    #联盟大使日任务  截图上传记录, 只包含火种数和上传截图所得积分
    def union_abd_task_daily(self,user_id):
        union_abd_task_daily = mongo.connectMongo('jinquan', 'union_abd_task_daily')
        res = union_abd_task_daily.find({'user_id':user_id})
        for i in res:
            print(i)

    # 联盟大使月任务 包含火种数以及本月目前所有已领取大使积分
    def union_abd_task_monthly(self,user_id):
        union_abd_task_monthly = mongo.connectMongo('jinquan', 'union_abd_task_monthly')
        res = union_abd_task_monthly.find({'user_id':user_id})
        for i in res:
            print(i)
    #联盟大使跟用户全部额外奖励
    def get_union_abd_unclaimed_point(self,union_abd_id,uid):
        key=f'abd_extra_point:{union_abd_id}:{uid}'
        res=jinquan_redis.get(key)
        print(res)

    #获取大使当天上传截图次数
    def get_union_abd_upload_game_count(self,union_abd_id):
        current_date=datetime.datetime.now().strftime('%Y-%m-%d')
        key=f'union_abd_upload_game_count_limit:{union_abd_id}:{current_date}'
        res=jinquan_redis.get(key)
        print(res)

if __name__ == '__main__':
    abd = UnionABD()
    abd.get_union_abd_upload_game_count('1452460951')
    abd.get_union_abd_unclaimed_point('1452460951','1478179721')