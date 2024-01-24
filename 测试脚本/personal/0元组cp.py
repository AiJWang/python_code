from 测试脚本.personal.mongconnect import mongoUtil

mongoUtil=mongoUtil()


def update_user_send_zero_gift_record(uid,receiver_uid_list=[],delete=0):
    user_send_zero_gift_record=mongoUtil.connectMongo('jinquan','user_send_zero_gift_record')
    if delete:
        user_send_zero_gift_record.delete_one({'user_id':uid})
    elif receiver_uid_list:
        result=list(user_send_zero_gift_record.find({'user_id':uid}))
        if len(result):
            user_record=result[0]
            male_send_user_ids=user_record.get('male_send_user_ids',None)
            if male_send_user_ids:
                male_send_user_ids=set(male_send_user_ids)-set(receiver_uid_list)
                count=user_send_zero_gift_record.update_one({'user_id':uid},{'$set':{'male_send_user_ids':list(male_send_user_ids)}}).modified_count
                print('修改条数：',count)

        else:
            print('未查到数据~')
    else:
        for i in user_send_zero_gift_record.find({'user_id':uid}):
            print(i)




if __name__ == '__main__':
    a=['1508726511']
    update_user_send_zero_gift_record('1515171171')