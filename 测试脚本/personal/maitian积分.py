# coding=utf-8
import datetime
import json
import os

import requests

os_cwd=os.getcwd()
cu_pa=os.path.dirname(os_cwd)

user_info={'cat':'361193928811','huoxing':'12684011','moon':'361194605131','qingwa':'19089051','water':'361196131361','c3c':'14364771','meinv':'14856711','maoer':'14945471','hel':'14913401'}



def cal_point(gift_num,anchor=None,target_user=None,target_user_type='SIGNED'):

    with open(os.path.join(cu_pa,'testdata','maitian.txt'),'r') as f:
        s=f.readlines()
        # print(f'历史数据：{s}')
    check_anchor=True
    lists=[]
    user_ratio= 0.3
    if target_user_type == 'SIGNED':
        user_ratio= 0.3
        on_mic_ratio = 0.1
    elif target_user_type == 'ANCHOR':
        user_ratio= 0.4
        on_mic_ratio = 0.05
        sanfang_ratio= 0.1
        mengxin_ratio= 0.05
    elif target_user_type == 'FAMILYLEADER':
        user_ratio= 0.5
        on_mic_ratio = 0.1

    for i in s:
        dic_s=json.loads(i)
        if user_info.get(target_user) in dic_s:
            if not anchor:
                check_anchor = False
                huoxing_dic_s=dic_s[user_info.get(target_user)]
                huoxing_dic_s['total_coin']=huoxing_dic_s['total_coin']+gift_num*10*user_ratio
                if target_user_type == 'MALE':
                    lists.append(dic_s)
                    print(f'收礼人积分：{huoxing_dic_s}')
                    continue
                huoxing_dic_s['total_onmic_poll']=huoxing_dic_s['total_onmic_poll']+gift_num*10*on_mic_ratio
                if target_user_type == 'ANCHOR':
                    huoxing_dic_s['total_sanfang']=huoxing_dic_s['total_sanfang']+gift_num*10*sanfang_ratio
                    huoxing_dic_s['mengxin']=huoxing_dic_s['mengxin']+gift_num*10*mengxin_ratio
                print(type(huoxing_dic_s['record']))
                # huoxing_dic_s['record'].append(f'花费金币总额：{gift_num}，积分总额：{gift_num*10*0.3}，积分余额：{gift_num*10*0.3}，积分池：{gift_num*10*0}')
                print(f'收礼人积分：{huoxing_dic_s}')
                lists.append(dic_s)
            else:
                if anchor ==target_user:
                    check_anchor = False
                    huoxing_dic_s=dic_s[user_info.get(target_user)]
                    huoxing_dic_s['total_coin']=huoxing_dic_s['total_coin']+gift_num*10*(user_ratio+0.05)
                    if target_user_type == 'MALE':
                        lists.append(dic_s)
                        print(f'收礼人积分：{huoxing_dic_s}')
                        continue
                    huoxing_dic_s['total_onmic_poll']=huoxing_dic_s['total_onmic_poll']+gift_num*10*on_mic_ratio
                    if target_user_type == 'ANCHOR':
                        huoxing_dic_s['total_sanfang']=huoxing_dic_s['total_sanfang']+gift_num*10*sanfang_ratio
                        huoxing_dic_s['mengxin']=huoxing_dic_s['mengxin']+gift_num*10*mengxin_ratio
                    print(type(huoxing_dic_s['record']))
                    # huoxing_dic_s['record'].append(f'花费金币总额：{gift_num}，积分总额：{gift_num*10*0.3}，积分余额：{gift_num*10*0.3}，积分池：{gift_num*10*0}')
                    print(f'收礼人积分：{huoxing_dic_s}')
                    lists.append(dic_s)
                else:
                    huoxing_dic_s=dic_s[user_info.get(target_user)]
                    huoxing_dic_s['total_coin']=huoxing_dic_s['total_coin']+gift_num*10*user_ratio
                    if target_user_type == 'MALE':
                        lists.append(dic_s)
                        print(f'收礼人积分：{huoxing_dic_s}')
                        continue
                    huoxing_dic_s['total_onmic_poll']=huoxing_dic_s['total_onmic_poll']+gift_num*10*on_mic_ratio
                    if target_user_type == 'ANCHOR':
                        huoxing_dic_s['total_sanfang']=huoxing_dic_s['total_sanfang']+gift_num*10*sanfang_ratio
                        huoxing_dic_s['mengxin']=huoxing_dic_s['mengxin']+gift_num*10*mengxin_ratio
                    print(type(huoxing_dic_s['record']))
                    # huoxing_dic_s['record'].append(f'花费金币总额：{gift_num}，积分总额：{gift_num*10*0.3}，积分余额：{gift_num*10*0.3}，积分池：{gift_num*10*0}')
                    print(f'收礼人积分：{huoxing_dic_s}')
                    lists.append(dic_s)
        elif check_anchor and user_info.get(anchor) in dic_s:
            huoxing_dic_s=dic_s[user_info.get(anchor)]
            huoxing_dic_s['total_coin']=huoxing_dic_s['total_coin']+gift_num*10*0.05
            print(f'主持人积分总额：{huoxing_dic_s}')
            lists.append(dic_s)
        else:
            lists.append(dic_s)

    # print(lists)
    with open(os.path.join(cu_pa,'testdata','maitian.txt'),'w') as f:
        for i in lists:
            f.write(json.dumps(i)+'\n')


def query_pool_data(uid):
    url=f'http://metis-maitian.diffusenetwork.com/score_pool/pool_stats?target_user_id={uid}&dt={datetime.datetime.now().date()}'
    print(url)
    resp=requests.get(url=url)
    print(resp.json())

def stest11():
    with open(os.path.join(cu_pa,'testdata','maitian1.txt'),'w') as f1:
        for i in range(5):
            f1.write(json.dumps({'ss':i})+'\n')




if __name__ == '__main__':
    user_type=['SIGNED','ANCHOR','FAMILYLEADER','MALE']
    cal_point(66,target_user='water',target_user_type=user_type[0])
