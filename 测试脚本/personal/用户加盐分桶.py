import hashlib
import json

import requests

yan = {'浪漫清单': 'sgfh', '唯一cp维持实验': 'uni_cp_mt','白银cp':'silver_cp','首日增加cp铃实验':'leave_room_cp_bell'}


def getBucket(uid, group_num=0):
    if not group_num:
        group_num = 30
    m = hashlib.md5(uid.encode(encoding='utf-8'))
    hexKey = int(m.hexdigest(), 16)
    return hexKey % group_num


# 通过重复注册，获取对应桶的uid
def get_user_id():
    pass


def register():
    url = 'http://poros-test.diffusenetwork.com/a-k8s/ccc/passport/qq_login?app=jinquan&pkg_name=com.liquid.poros&biz=jinquan&version_name=2.0.3.3&device_serial=unknown&wifi_proxy=true&user_id=1412634311&wifi_mac_addr=unknow&wifi_vpn=false&platform_name=Android'
    body = {
        "access_token": "C6BC2C9E052E66DDC62E04EEB84C2DC8",
        "share_id": "",
        "openid": "2C4EB4497953CFFC81032F1579A466F7",
        "token": ""
    }
    # 设置性别
    url1 = 'http://poros-test.diffusenetwork.com/a-k8s/service/views/user/register?channel_name=unknown_channel&app=jinquan&hotfix_version=&nonce_str=e77f232d-bb78-4ccd-a75a-7ab85029792c&own_family_id=&device_id=b6f53a88-4f34-35b2-9d7e-9d7ede5e5260&sign=Q2FTj3v7y8J0X1CYrUC6iQ&Latitude=&Longitude=&et=1699346863300&pkg_name=com.liquid.poros&biz=jinquan&version_name=2.0.3.3&device_serial=unknown&wifi_proxy=true&mac_addr=020000000000&user_id=1412947791&wifi_mac_addr=unknow&wifi_vpn=false&platform_name=Android&imei=&own_union_id=&android_id=e95772b6217fbbfc&oaid=8a2499952ab55d19';
    gender = {
        "gender": 1,
        "token": "c2514e10-d094-465d-810e-becc3c9999c1"
    }
    # 设置生日
    birthday = {
        "birthday": "2000-2-1",
        "token": "c2514e10-d094-465d-810e-becc3c9999c1"
    }
    # 设置游戏--不玩游戏
    game_info = {
        "game_info": {},
        "token": "c2514e10-d094-465d-810e-becc3c9999c1"
    }


def del_v3(*args,**kwargs):
    url = 'http://poros-test.diffusenetwork.com/a-k8s/ccc/passport/del_v3?app=jinquan&pkg_name=com.liquid.poros&biz=jinquan&version_name=2.0.3.3&device_serial=unknown&wifi_proxy=true&user_id=1412634311&wifi_mac_addr=unknow&wifi_vpn=false&platform_name=Android'
    token = {"token": kwargs['token']}
    resp = requests.post(url=url, data=json.dumps(token))
    print(resp)
    print(resp.text)
    result = json.loads(resp.text)
    print(resp)
    print(resp.status_code)
    print(resp.cookies)
    assert resp.status_code and result['code'] == 0 and result['msg'] == 'ok'


if __name__ == '__main__':
     print(getBucket("297212492491" + yan['首日增加cp铃实验'], 100))
