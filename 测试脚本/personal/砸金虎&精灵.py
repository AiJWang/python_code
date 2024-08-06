import json
import os
import time
from datetime import datetime

import requests

from 测试脚本.personal.common import Common_Function
from 测试脚本.personal.mongconnect import mongoUtil
# 在 gold_dragon 表里面，type_id 为1 表示金龙， 为2 是精灵
'''
1. 功能开关，在进圈库，elves表中 biz list
2. 获得开关  在ab-test2 中精灵实验（搜索精灵即可）
'''
os_cwd=os.getcwd()
cu_pa=os.path.dirname(os_cwd)
class Golden(Common_Function):
    host='http://advanced-poros.test.diffusenetwork.net'

    def make_data(self,user_id,cp_user_id,app='jinquan',num=2,type_id=2):
        '''插入 num 数量的精灵、金龙，type_id 为1 表示金龙， 为2 是精灵'''
        cp_tag=f'{user_id}_{cp_user_id}' if cp_user_id>user_id else f'{cp_user_id}_{user_id}'
        data_dict={
            "biz": app,
            "app": app,
            "user_id": user_id,
            "cp_user_id": cp_user_id,
            "cp_tag": cp_tag,
            "dragon_num":num,
            "deleted":0,
            "type_id": type_id,
            'create_time': datetime.now(),
            'update_time': datetime.now(),
            'delete_time': datetime(1970, 1, 1, 0, 0)
        }
        gold_dragon=mongoUtil().connectMongo('jinquan_admin','gold_dragon',db='backpack')
        print(data_dict)
        res=list(gold_dragon.find({'user_id':user_id,'cp_user_id':cp_user_id,'type_id':type_id,'deleted':0}))
        if res:
            count=gold_dragon.update_many({'user_id':user_id,'cp_user_id':cp_user_id,'type_id':type_id,'deleted':0}, {'$set': {'dragon_num': num}}).modified_count
            print(f'count:{count}')
        else:
            ss=gold_dragon.insert_one(data_dict).inserted_id
            print(f'插入数据{ss}')

    def get_config_info(self,elves_id=2,rank=None):
        '''获取配置信息'''
        elves_rank=mongoUtil().connectMongo('jinquan','elves_rank')
        if rank:
            res=list(elves_rank.find({'elves_id':elves_id,'rank':rank}))
            if res:
                return res[0]
        else:
            res=list(elves_rank.find({'elves_id':elves_id}))
            if res:
                res.sort(key=lambda x:x['rank'],reverse=True)
                return res

    def golden_tiger_old_launch(self,user_id,cp_user_id,num=99,type_id=2):
        '''砸num数量的精灵  type_id 为1 表示金龙， 为2 是精灵'''
        user_token=self.get_token(user_id)
        url=f'{self.host}/ccc/service/views/goldentiger/old_launch?hotfix_version=0&nonce_str=b46fc613-4010-47ba-b1ee-4c4ba9d68496&sign=heNXsNisIJk9QT7IkKwd8A&Latitude=&biz=jinquan&wifi_proxy=true&mac_addr=020000000000&wifi_mac_addr=unknow&wifi_vpn=false&platform_name=Android&oaid=55C8CC72D0AC497DB5167309473D6759b66a5e6a043539043add1a1120aca9cc&channel_name=unknown_channel&app=jinquan&Longitude=&et=1721027068300&pkg_name=com.liquid.poros&version_name=2.1.1.9&device_serial=unknown&user_id={user_id}&imei=&x-env-flow=common-test'
        timex=1
        elves_rank=self.get_config_info(type_id)
        max_level=elves_rank[0]['rank']
        ta={}

        total=0
        name='精灵' if type_id==2 else '金龙'
        not_write_file=False
        try:
            with open(os.path.join(cu_pa,'testdata','golden.txt'),'w') as f:
                while num>0:
                    print(f'砸第{timex}个{name}')
                    level=0
                    body={
                        "elves_id": type_id,
                        "token": user_token
                    }
                    print(f'level:{level},max_level:{max_level}')
                    fail_level=[]
                    while level<max_level:
                        try:
                            if level==0:
                                resp=requests.post(url,json=body).json()
                                print(resp)
                                if resp.get('code')==17039 and resp.get('msg')=='余额不足':
                                    self.get_money(user_id)
                                    continue
                                if resp.get('code')==20000 and resp.get('msg')=='背包内剩余资源不足':
                                    self.make_data(user_id,cp_user_id,app='jinquan',num=num+2,type_id=type_id)
                                    continue
                                if resp.get('code')!=0:
                                    continue
                                rec_id=resp.get('data').get('rec_id')
                                body['rec_id']=rec_id

                            else:
                                resp=requests.post(url,json=body).json()
                                if resp.get('code')==17039 and resp.get('msg')=='余额不足':
                                    self.get_money(user_id)
                                    continue
                                if resp.get('code')==20000 and resp.get('msg')=='背包内剩余资源不足':
                                    #默认设置精灵
                                    self.make_data(user_id,cp_user_id,app='jinquan',num=num+2,type_id=type_id)
                                    continue
                                print(resp)
                        except Exception as e:
                            print(e)
                            time.sleep(1)
                            continue
                        if resp.get('code')!=0:
                            continue
                        data=resp.get('data')
                        level=data.get('level')
                        cut_radio=data.get('cut_radio')
                        is_success=data.get('is_success')
                        if level not in fail_level:
                            total+=1
                            if level_info:=ta.get(level):
                                if is_success:
                                    if level_info.get('suc'):
                                        level_info['suc']+=1
                                    else:
                                        level_info['suc']=1
                                else:
                                    fail_level.append(level)
                                    if level_info.get('fail'):
                                        level_info['fail']+=1
                                    else:
                                        level_info['fail']=1
                            else:
                                if is_success:
                                    ta[level]={'suc':1}
                                else:
                                    fail_level.append(level)
                                    ta[level]={'fail':1}
                            if ta.get(f'cut_radio_{cut_radio}'):
                                ta[f'cut_radio_{cut_radio}']+=1
                            else:
                                ta[f'cut_radio_{cut_radio}']=1
                        if data.get('is_break'):
                            break
                        time.sleep(0.1)
                    num-=1
                    timex+=1
                ta['total']=total
                f.write(json.dumps(ta,ensure_ascii=False,indent=4)+'\n')
                self.anylize_golden_tiger_result(type_id,ta)
                print(f'结果：{ta}')
        except Exception as e:
            not_write_file=True
            print(e)
        finally:
            if not_write_file:
                with open(os.path.join(cu_pa,'testdata','golden.txt'),'w') as f:
                    f.write(json.dumps(ta,ensure_ascii=False,indent=4)+'\n')


    def anylize_golden_tiger_result(self,type_id=2,result=None):
        '''解析砸金龙、精灵结果，type_id 为1 表示金龙， 为2 是精灵,result 为结果'''
        max_level=7 if type_id==1 else 15
        if not result:
            with open(os.path.join(cu_pa,'testdata','golden.txt'),'r') as f:
                ta=dict(json.loads(f.read().strip()))
                print(ta)
                for i in range(1,max_level+1):
                    if i not in ta :
                        i=str(i)
                    if i not in ta:
                        print(f'{i}级：未能升级')
                        continue
                    suc_in=ta.get(i).get('suc',0)
                    fail_in=ta.get(i).get('fail',0)
                    total_level=suc_in+fail_in
                    suc_rate=round(suc_in/total_level,2) if total_level else 0
                    print(f'{i}级：成功{suc_in}次，失败{fail_in}次，成功率{suc_rate}，理论成功率{self.get_config_info(type_id,int(i)).get("success_rate")/100}')
                keys=list(ta.keys())
                for k in keys:
                    if type(k)==str and k.startswith('cut_radio_'):
                        print(f'礼物币倍率{k.split("_")[2]}概率：{round(ta.get(k)/ta.get("total"),2)}')
        else:
            for i in range(1,max_level+1):
                if i not in result:
                    print(f'{i}级：未能升级')
                    continue
                suc_in=result.get(i).get('suc',0)
                fail_in=result.get(i).get('fail',0)
                total_level=suc_in+fail_in
                suc_rate=round(suc_in/total_level,2) if total_level else 0
                print(f'{i}级：成功{suc_in}次，失败{fail_in}次，成功率{suc_rate}，理论成功率{self.get_config_info(type_id,i).get("success_rate")/100}')
            keys=list(result.keys())
            for k in keys:
                if type(k)==str and k.startswith('cut_radio_'):
                    print(f'礼物币倍率{k.split("_")[2]}概率：{round(result.get(k)/result.get("total"),2)}')
if __name__ == '__main__':
    user_info={'qingwa':'1881255741','water':'1881270491','c3c':'1880857211','qu':'1881119701'}
    g = Golden()
    # g.golden_tiger_info('1788620761')
    #g.make_data('1881119701','1880857211',num=10)
    #g.golden_tiger_info('1867291051')
    g.golden_tiger_old_launch('1881255741','1480845661',num=2,type_id=1)
    #g.anylize_golden_tiger_result(type_id=1)




