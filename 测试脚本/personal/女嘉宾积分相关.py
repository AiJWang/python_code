from 测试脚本.personal.mongconnect import mongoUtil

mongoUtil = mongoUtil()


def del_signed_voice_female_monthly(uid, delete=0):
    signed_voice_female_monthly = mongoUtil.connectMongo('account', 'signed_voice_female_monthly')
    res = list(signed_voice_female_monthly.find({'user_id': uid, 'task_date': '2024-02'}).sort([('_id', -1)]))
    if len(res):
        print(res[0].get('total_gift_point'))
        if delete:
            rows = signed_voice_female_monthly.update_one({'user_id': uid, 'task_date': '2024-02'},
                                                          {'$set': {'total_gift_point': 0}}).modified_count
            print(f'修改数据：{rows} 条')

    else:
        signed_voice_room_achor_monthly = mongoUtil.connectMongo('account', 'signed_voice_room_achor_monthly')
        res = list(signed_voice_room_achor_monthly.find({'user_id': uid, 'task_date': '2024-02'}).sort([('_id', -1)]))
        if len(res):
            print(res[0].get('total_gift_point'))
            if delete:
                rows = signed_voice_room_achor_monthly.update_one({'user_id': uid, 'task_date': '2024-02'},
                                                              {'$set': {'total_gift_point': 0}}).modified_count
                print(f'修改数据：{rows} 条')
        print('')


if __name__ == '__main__':
    cat = '1452460951'
    water = '1508726511'
    huoxing='1534691741'
    del_signed_voice_female_monthly(cat,delete=0)
