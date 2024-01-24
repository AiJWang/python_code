import hashlib
import json

import requests

from util.yamlUtil import YmlTuil

yan = {'浪漫清单': 'sgfh',
       '唯一cp维持实验': 'uni_cp_mt',
       '白银cp': 'silver_cp',
       '首日增加cp铃实验': 'leave_room_cp_bell',
       '延迟逼客': 'room_interactive_value',
       '女用户展示照片C端转化实验': 'jdus',
       '唯一cp积分池': 'interaction_time_test',
       '新女嘉宾kpi': 'new_voice_female'}


# 分桶
def getBucket(uid, group_num=100):
    if not group_num:
        group_num = 30
    m = hashlib.md5(uid.encode(encoding='utf-8'))
    hexKey = int(m.hexdigest(), 16)
    return hexKey % group_num


if __name__ == '__main__':
    print(getBucket("317287952511" + yan['新女嘉宾kpi']))

