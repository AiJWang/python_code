from 测试脚本.personal.mongconnect import mongoUtil


def get_belong_info(*args):
    '查询归属关系'
    cp_belong_relation=mongoUtil().connectMongo('organization_service_test','cp_belong_relation')
    if args:
        res=list(cp_belong_relation.find({'$or':[{'user_ids_key':f'{args[0]}_{args[1]}'},{'user_ids_key':f'{args[1]}_{args[0]}'}]}))
    else:
        res=list(cp_belong_relation.find().sort([('_id',-1)]).limit(10))
    for i in res:
        print(i)


if __name__ == '__main__':
    get_belong_info()