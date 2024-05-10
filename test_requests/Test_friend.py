import pytest as pytest
import requests as requests

from util.yamlUtil import YmlTuil


class Test_FriendGet:
    #设置成统一的会话，这样header就是公用一个了
    session=requests.session()
    # def setup(self):
    #     print("每条用例之前执行")
    # def teardown(self):
    #     print("每条用例之后执行")
    # def setup_class(self):
    #     print("类之前执行")
    # def teardown_class(self):
    #     print("类之后执行")
    #标记这条用例是冒烟的用例
    @pytest.mark.smoke
    def test_online_friend(self,connect_database):
        url='http://metis-test.diffusenetwork.com/bbb/friend/online?token=be00e3f8-be52-466a-bdc3-b29f7f134447&hotfix_version=&nonce_str=24607576-0f5e-4983-82e5-8c7cdf2db110&own_family_id=97895279&sign=Ab53iTp4G3nWv7pQflJiXg&Latitude=&client_type=leader&biz=jinquan&wifi_proxy=true&mac_addr=020000000000&wifi_mac_addr=unknow&wifi_vpn=false&platform_name=Android&oaid=8a2499952ab55d19&channel_name=unknown_channel&app=jinquan_leader&device_id=2fcbcfa0-304a-3fb5-b8bb-57b326da1793&Longitude=&et=1695702565300&pkg_name=com.liquid.poros.pro&version_name=2.0.1.7&device_serial=unknown&user_id=1071793351&imei=&own_union_id=615015c215703a6fd28e39d4&android_id=c2c6b1fd8621b9ee'
        resp=Test_FriendGet.session.get(url)
        print(resp.json())

    def test_friend_diff_list(self):
        url='http://metis-test.diffusenetwork.com/bbb/friend/diff_list?version_id=651131c9186eb7c656f2a966&token=be00e3f8-be52-466a-bdc3-b29f7f134447&hotfix_version=&nonce_str=31b6e660-6fdb-4735-96b4-9572657c3e6b&own_family_id=97895279&sign=DZMuioAZ4AKBGYnMVp2UHg&Latitude=&client_type=leader&biz=jinquan&wifi_proxy=true&mac_addr=020000000000&wifi_mac_addr=unknow&wifi_vpn=false&platform_name=Android&oaid=8a2499952ab55d19&channel_name=unknown_channel&app=jinquan_leader&device_id=2fcbcfa0-304a-3fb5-b8bb-57b326da1793&Longitude=&et=1695702565300&pkg_name=com.liquid.poros.pro&version_name=2.0.1.7&device_serial=unknown&user_id=1071793351&imei=&own_union_id=615015c215703a6fd28e39d4&android_id=c2c6b1fd8621b9ee'
        resp=Test_FriendGet.session.get(url)
        YmlTuil().writeYml({'current_version_id':resp.json()['data']['current_version_id']})
        print(resp.json())

    #调用前置函数，pytest.fixtrue()
    def test_kin_lsit(self):
        url='http://poros-test.diffusenetwork.com/service/kin/kin_list?target_user_id=1071793351&token=be00e3f8-be52-466a-bdc3-b29f7f134447&hotfix_version=&nonce_str=8180b9c0-b767-45cb-a31f-05364c982962&own_family_id=97895279&sign=5KaVcTbeOj4TBZJ0en-i2Q&Latitude=&client_type=leader&biz=jinquan&wifi_proxy=true&mac_addr=020000000000&wifi_mac_addr=unknow&wifi_vpn=false&platform_name=Android&oaid=8a2499952ab55d19&channel_name=unknown_channel&app=jinquan_leader&device_id=2fcbcfa0-304a-3fb5-b8bb-57b326da1793&Longitude=&et=1695705755300&pkg_name=com.liquid.poros.pro&version_name=2.0.1.7&device_serial=unknown&user_id=1071793351&imei=&own_union_id=615015c215703a6fd28e39d4&android_id=c2c6b1fd8621b9ee'
        resp=Test_FriendGet.session.get(url)
        print(YmlTuil().readYml())
        print('-'*10)
        print(resp.json())
    def test(self):
        print('first test')


if __name__ == '__main__':
    aa=getattr('Test_FriendGet','test')
    print(aa)