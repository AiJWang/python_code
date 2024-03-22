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
       '新女嘉宾kpi': 'new_voice_female',
       '0元加好友':'zero_cost_add_friend',
       '主动铃':'cp_bell_exchange',
       '0元组cp老用户实验':'scbt',
       '女嘉宾白银cp陪伴实验':'accompany_b_task',
       '主持人白银cp陪伴实验':'assistance_task'
       }


# 分桶
def getBucket(uid, group_num=100):
    if not group_num:
        group_num = 30
    m = hashlib.md5(uid.encode(encoding='utf-8'))
    hexKey = int(m.hexdigest(), 16)
    return hexKey % group_num


if __name__ == '__main__':
    qu='340628222151'
    ge='1568748251'
    iq='341532327241'
    sun='1550591221'
    C3C='1550628211'
    print(getBucket(iq+yan['主持人白银cp陪伴实验']))
    print(getBucket(iq + yan['女嘉宾白银cp陪伴实验']))

