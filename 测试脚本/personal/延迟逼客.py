


from 测试脚本.personal.mongconnect import mongoUtil

mongoUtil=mongoUtil()

#女嘉宾删除积分记录  type：92 延迟逼客奖励
def delete_point_record(query):
    female_guest_point_record=mongoUtil.connectMongo('account','female_guest_point_record')

    res=female_guest_point_record.delete_many(query)
    print('删除数据条数：',res.deleted_count)

if __name__ == '__main__':
    query={'user_id':{'$in':['1452460951','1484693641','1486273331','1480845661','1406867451']},'type':92}
    delete_point_record(query)
