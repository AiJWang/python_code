import json
import time
from random import choice

import requests

from 测试脚本.personal.common import Common_Function
from 测试脚本.personal.常規 import update_user_game_energy


class Gift(Common_Function):
    url_prb = "?pkg_name=%s&biz=%s&version_name=%s&sign=qGNbDeP6wSvYb34QHnCKQQ" % (
    'com.liquid.poros.pro', "jinquan", "2.0.6.9")
    url_prc = "?pkg_name=%s&biz=%s&version_name=%s&sign=qGNbDeP6wSvYb34QHnCKQQ" % (
    "com.liquid.poros", "jinquan", "2.0.6.9")
    family_type={'union':'50628589','family':'97895279','wenzipindao':'72672889','team':'50331289'}

    def send_gift_target_b(self, ress):
        token = self.get_token(ress.get('uid'))
        url = 'http://advanced-poros.test.diffusenetwork.net/service/user/send_gift' + self.url_prc
        gift_list=self.get_gift_list()
        send_gift_list=[]
        for gift in gift_list:
            if gift.get('add_score') ==ress.get('add_score'):
                send_gift_list.append(gift)
        gift=choice(send_gift_list)
        gift_id=gift.get('id')
        print('礼物名称：',gift.get('name'),gift.get('animation_name'))
        param = {
            "family_position": "family",
            "family_id": self.family_type.get(ress.get('family_position')),
            "num": ress.get('num'),
            "gift_list_name": "",
            "gift_id": gift_id,
            "gift_coin_first": True,
            "target_user_id": ress.get('target_user_id'),
            "to_anchor": False,
            "is_gift_boost": True,
            "token": token,
            "scene": ""
        }
        res = requests.request(method='POST', url=url, data=json.dumps(param))
        if res.json().get('msg') == '余额不足':
            print(self.get_money(ress.get('uid')))
            res = requests.request(method='POST', url=url, data=json.dumps(param))
        print(res.status_code, res.json())

    def send_gift_target_c(self, ress):
        token = self.get_token(ress.get('uid'))
        url = 'http://advanced-poros.test.diffusenetwork.net/service/user/send_gift' + self.url_prb
        # gift_list=self.get_gift_list()
        # send_gift_list=[]
        # for gift in gift_list:
        #     if gift.get('add_score') ==ress.get('add_score'):
        #         send_gift_list.append(gift)
        # gift=choice(send_gift_list)
        # gift_id=gift.get('id')
        #print('礼物名称：',gift.get('name'),gift.get('animation_name'))
        param = {
            "family_position": "family",
            "family_id": self.family_type.get(ress.get('family_position')),
            "num": ress.get('num'),
            "gift_list_name": "",
            "gift_id": ress.get('gift_id'),
            "target_user_id": ress.get('target_user_id'),
            "to_anchor": False,
            "is_gift_boost": True,
            "token": token,
            "scene": ""
        }
        res = requests.request(method='POST', url=url, data=json.dumps(param))
        if res.json().get('msg') == '余额不足':
            print(self.get_money(ress.get('uid')))
            res = requests.request(method='POST', url=url, data=json.dumps(param))
        print(res.status_code, res.json())

    def get_gift_list(self):
        url='http://advanced-poros.test.diffusenetwork.net/service/views/gift/list?source=MSG&target_user_id=1508726511&token=0843052e-e2ad-4509-aca3-42c56400a0ab'
        res=requests.request(method='get',url=url)
        print(res.json())
        return res.json().get('data').get('gifts')

if __name__ == '__main__':
    # 火星：1508472331   水星：1508726511     猫猫：1452460951  月亮：1480845661
    # 我们的歌：1489653311    iqoo:1488701421    我们的曲：1509489771   C3C：1498619021
    # param_to_b = {
    #     'family_position': 'family',
    #     'num': 1,
    #     'add_score': 9999,
    #     'uid': '1509680431',
    #     'target_user_id': '1508726511'
    # }
    # Gift().send_gift_target_b(param_to_b)

    #update_user_game_energy(['1490781851','1489653311','1452460951','1480845661','1498619021'],180)
    #time.sleep(60)
    for i in [109, 110, 111, 112]:
        param_to_c = {
            'family_position': 'union',
            'num': 1,
            'add_score': 9999,
            'uid': '1565519381',
            'gift_id': i,
            'target_user_id': '1417432981'
        }
        Gift().send_gift_target_c(param_to_c)


    #
    # time.sleep(30)
    #
    # param_to_b = {
    #     'family_position': 'union',
    #     'num': 1,
    #     'add_score': 666,
    #     'uid': '1488701421',
    #     'target_user_id': '1452460951'
    # }
    # Gift().send_gift_target_b(param_to_b)

