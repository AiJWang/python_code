import hashlib
import json

import requests

from util.yamlUtil import YmlTuil

yan = {'浪漫清单': 'sgfh', '唯一cp维持实验': 'uni_cp_mt', '白银cp': 'silver_cp', '首日增加cp铃实验': 'leave_room_cp_bell','延迟逼客':'room_interactive_value','女用户展示照片C端转化实验':'jdus','唯一cp积分池':'interaction_time_test','新女嘉宾kpi':'new_voice_female'}

#分桶
def getBucket(uid, group_num=0):
    if not group_num:
        group_num = 30
    m = hashlib.md5(uid.encode(encoding='utf-8'))
    hexKey = int(m.hexdigest(), 16)
    return hexKey % group_num


# 通过重复注册，获取对应桶的uid
def get_user_id():
    pass

comman_path='channel_name=unknown_channel&app=jinquan&hotfix_version=&nonce_str=9e75a683-2c4d-4570-81ad-42e672c9bc8d&own_family_id=&device_id=b6f53a88-4f34-35b2-9d7e-9d7ede5e5260&sign=9iDG21PL_sgqPZHaqh1-HQ&Latitude=&Longitude=&et=1702183772300&pkg_name=com.liquid.poros&biz=jinquan&version_name=2.0.4.9&device_serial=unknown&wifi_proxy=true&mac_addr=020000000000&user_id=&wifi_mac_addr=unknow&wifi_vpn=false&platform_name=Android&imei=&own_union_id=&android_id=e95772b6217fbbfc&oaid=8a2499952ab55d19'

def register():
    url = 'http://poros-test.diffusenetwork.com/ccc/passport/wechat_login?'+comman_path
    body = {
        "share_id": "",
        "code": "001i4QGa1NkEvG0fshIa1iTGYp2i4QGL",
        "token": ""
    }
    resp = requests.post(url=url, data=json.dumps(body))
    print('register',resp.text)
    result = json.loads(resp.text)
    return result


arg={}
arg['token']='2c979b6b-d442-4198-9c59-1738d49e5104'
arg['uid']='1454961411'
comman_path_other='channel_name=unknown_channel&app=jinquan&hotfix_version=&nonce_str=57f8a2d8-c4c6-4015-80a2-440bd2ac94dd&own_family_id=&device_id=b6f53a88-4f34-35b2-9d7e-9d7ede5e5260&sign=rc0gbzv4b9sTWo4O-owhzw&Latitude=&Longitude=&et=1702183886300&pkg_name=com.liquid.poros&biz=jinquan&version_name=2.0.4.9&device_serial=unknown&wifi_proxy=true&mac_addr=020000000000&user_id='+arg['uid']+'&wifi_mac_addr=unknow&wifi_vpn=false&platform_name=Android&imei=&own_union_id=&android_id=e95772b6217fbbfc&oaid=8a2499952ab55d19'

def set_info(*args):
    # 设置性别
    url = 'http://poros-test.diffusenetwork.com/service/views/user/register?' + comman_path_other
    gender = {
        "gender": 1,
        "token": arg['token']
    }
    gender = requests.post(url=url, data=json.dumps(gender))
    print('gender',gender.text)
    # 设置生日
    birthday = {
        "birthday": "2000-2-1",
        "token": arg['token']
    }
    birthday = requests.post(url=url, data=json.dumps(birthday))
    print('gender',birthday.text)
    # 设置游戏--不玩游戏
    game_info = {
        "game_info": {},
        "token": arg['token']
    }
    game_info = requests.post(url=url, data=json.dumps(game_info))
    print('gender',game_info.text)



def login_check(*args, **kwargs):

    url = 'http://poros-test.diffusenetwork.com/service/login/check/identityAuth?'+comman_path_other
    token = {"token": kwargs['token']}
    resp = requests.post(url=url, data=json.dumps(token))
    print('login_check',resp.text)
    result = json.loads(resp.text)
    return result


def del_verify_code(*args, **kwargs):

    url = 'http://poros-test.diffusenetwork.com/ccc/passport/del_verify_code?'+comman_path_other
    params = {"sms_code": "1234", "token": kwargs['token']}
    resp = requests.post(url=url, data=json.dumps(params))
    print('del_verify_code',resp.text)
    return json.loads(resp.text)


def del_v3(*args, **kwargs):

    url = 'http://poros-test.diffusenetwork.com/ccc/passport/del_v3?'+comman_path_other
    token = {"token": kwargs['token']}
    if kwargs.get('sms_code',None):
        token['sms_code'] = kwargs['sms_code']
    print("del_v3", token)
    resp = requests.post(url=url, data=json.dumps(token))
    print(resp)
    print('del_v3',resp.text)
    result = json.loads(resp.text)
    assert resp.status_code and result['code'] == 0 and result['msg'] == 'ok'


if __name__ == '__main__':
    print(getBucket("1509039221" + yan['唯一cp积分池'], 100))

    #register()
    # comman_params = {'version': '2.0.4.9', }
    # set_info(arg)
    # phone_info=login_check(token=arg['token'])
    # if phone_info['data']['phone_auth']:
    #     del_verify_code(token=arg['token'])
    #     del_v3(token=arg['token'], sms_code='1234')
    # else:
    #     del_v3(token=arg['token'])

