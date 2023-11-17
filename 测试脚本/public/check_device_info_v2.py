# coding=utf-8
import os
import time
import pymongo
import datetime
import subprocess

COMMAND = 'adb logcat -v threadtime'  # 常量
cur_path = os.path.dirname(os.path.realpath(__file__))
# log_path = os.path.join(os.path.dirname(cur_path), 'device_info')
log_path = cur_path


class LogcatCathcher(object):
    def __init__(self):
        self.log_file = None
        self.hf = None

    def get_logcat(self):
        self._create_hf()
        self.p_obj = subprocess.Popen(
            args=COMMAND,
            stdin=None, stdout=self.hf,
            stderr=self.hf, shell=False)

    def _create_hf(self):
        now_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        log_name = 'Logcat_' + now_time + '.txt'
        print(f'日志文件为：{log_name}')
        self.log_file = os.path.join(log_path, log_name)
        # 因为没指定具体路径，默认就是在当前脚本运行的路径下创建这个log_file
        self.hf = open('%s' % self.log_file, 'wb')

    def catch_logcat(self, step):
        # 清理缓存log
        os.system('adb logcat -c')
        self.get_logcat()
        print('日志抓取中... ')
        if step == 1:
            print('请完成以下动作：请退出登录，清理后台，重新打开应用，并登录成功。')
            judge_text = '1'
        elif step == 3:
            print('请完成以下动作：请清理后台，重新打开应用，并登录成功。')
            judge_text = '3'
        # 持续询问是否需要停止截取
        judge = input(f'如果已操作完毕，请输入[{judge_text}]:')
        while judge != judge_text:
            print(f'输入错误, 请输入[{judge_text}]')
            judge = input(f'如果已操作完毕，请输入[{judge_text}]:')
        else:
            if judge == judge_text:
                time.sleep(2)  # 多抓取2秒
                self.p_obj.terminate()
                self.p_obj.kill()
                self.hf.close()  # 关闭文件句柄
        return os.path.abspath(self.log_file)

    def check_log_file(self, step):
        self.online_found = False
        device_url = '/user/device_info'
        qq_url, wechat_url = '/user/qq_login', '/user/wechat_login'
        if step == 1:
            print(f'分析日志，获取待删除设备信息中... ')
        elif step == 3:
            print(f'分析日志，获取上传设备信息中... ')
        with open(self.log_file, mode='r', encoding='utf-8') as f:
            # with open('Logcat_20220510_210705.txt', mode='r', encoding='utf-8') as f:
            str_list, qq_list, wechat_list = [], [], []
            user_id_list = []
            self.env = 'test'
            for line in f.readlines():
                if f'{device_url}?' in line and '<-- 200' in line:
                    if 'oaid=&' in line and 'imei&' in line:
                        pass
                    else:
                        str_list.append(line.split('?')[1])
                        if 'noah-test' in line or 'testporos' in line or 'poros-test' in line:
                            self.env = 'test'
                        elif 'diffusenetwork' in line:
                            self.env = 'online'
                elif f'{qq_url}?' in line and '<-- 200' in line:
                    if 'oaid=&' in line and 'imei&' in line:
                        pass
                    else:
                        qq_list.append(line.split('?')[1])
                elif f'{wechat_url}?' in line and '<-- 200' in line:
                    if 'oaid=&' in line and 'imei&' in line:
                        pass
                    else:
                        wechat_list.append(line.split('?')[1])
                elif 'user_id=' in line and 'user_id=&' not in line:
                    user_id = line.split('user_id=')[1].split('&')[0]
                    if user_id.isdigit():
                        user_id_list.append(user_id)
            # 双重验证
            if str_list:
                if qq_list:
                    double_check = True
                    str_list.extend(qq_list)
                    if step == 3:
                        print(f'接口：[{qq_url}] 与 [{device_url}] 已上传设备信息成功！！')
                elif wechat_list:
                    double_check = True
                    str_list.extend(wechat_list)
                    if step == 3:
                        print(f'接口：[{wechat_url}] 与 [{device_url}] 已上传设备信息成功！！')
            # print(self.env)
            oaid_list, imei_list = [], []
            for index, url in enumerate(str_list):
                if 'device_id=' in url and 'app=' in url:
                    device_id = url.split('device_id=')[1].split('&')[0]
                    app = url.split('app=')[1].split('&')[0]
                    if device_id != 'device_id_not_init' and len(device_id) > 20:
                        if 'oaid=' in url:
                            if not url.split('oaid=')[1].startswith('&'):
                                oaid = url.split('oaid=')[1].split('&')[0]
                                if oaid != '00000000000000000000000000000000' and \
                                    oaid != '00000000-0000-0000-0000-000000000000':
                                    oaid_list.append((oaid, device_id, app))
                        if 'imei=' in url:
                            if not url.split('imei=')[1].startswith('&'):
                                imei = url.split('imei=')[1].split('&')[0]
                                if imei.isdigit() and len(imei) == 15 and imei != '000000000000000':
                                    imei_list.append((imei, device_id, app))
            self.oaid, self.imei = None, None
            if oaid_list:
                self.oaid = list(set(oaid_list))[0]
            if imei_list:
                self.imei = list(set(imei_list))[0]
            if user_id_list:
                self.user_id = list(set(user_id_list))[0]
            status = True
            if step == 1 and self.env == 'online':
                print_str = '待删除设备信息已找到，线上环境，数据无法删除，信息如下：\n'
                if self.oaid and self.imei:
                    print(
                        f'{print_str}oaid = [{self.oaid[0]}], device_id = [{self.oaid[1]}]\n\
                        imei = [{self.imei[0]}], device_id = [{self.imei[1]}]')
                    self.online_found = True
                elif self.oaid:
                    print(f'{print_str}oaid = [{self.oaid[0]}], device_id = [{self.oaid[1]}]')
                    self.online_found = True
                elif self.imei:
                    print(f'{print_str}imei = [{self.imei[0]}], device_id = [{self.imei[1]}]')
                    self.online_found = True
                else:
                    print(f'待删除设备信息未找到！')
                status = False
            elif step == 1:
                print_str = '待删除设备信息已找到，信息如下：\n'
                if self.oaid and self.imei:
                    print(
                        f'{print_str}oaid = [{self.oaid[0]}], device_id = [{self.oaid[1]}]\n\
                        imei = [{self.imei[0]}], device_id = [{self.imei[1]}]')
                elif self.oaid:
                    print(f'{print_str}oaid = [{self.oaid[0]}], device_id = [{self.oaid[1]}]')
                elif self.imei:
                    print(f'{print_str}imei = [{self.imei[0]}], device_id = [{self.imei[1]}]')
                else:
                    print(f'待删除设备信息未找到！')
                    status = False
            elif step == 3 and double_check:
                print_str = '设备信息上传成功，信息如下：\n'
                if self.oaid and self.imei:
                    print(
                        f'{print_str}oaid = [{self.oaid[0]}], device_id = [{self.oaid[1]}]\n\
                        imei = [{self.imei[0]}], device_id = [{self.imei[1]}]')
                elif self.oaid:
                    print(f'{print_str}oaid = [{self.oaid[0]}], device_id = [{self.oaid[1]}]')
                elif self.imei:
                    print(f'{print_str}imei = [{self.imei[0]}], device_id = [{self.imei[1]}]')
                else:
                    print('设备信息上传失败！')
                    status = False
            return status

    def check_mongo_data(self, step):
        # 测试数据库
        mongodb_test = {'uri': 'mongodb://%s:%s@s-2ze804aac801b914-pub.mongodb.rds.aliyuncs.com:3717/jinquan',
                        'username': 'poros_test', 'password': '6nKBKbCdBxizNRQJ'}
        uri_test = mongodb_test.get('uri') % (mongodb_test.get('username'), mongodb_test.get('password'))
        # 线上数据库
        # mongodb_online = {
        #     'uri': 'mongodb://%s:%s@s-2ze1de83b7e68e94-pub.mongodb.rds.aliyuncs.com:3717/?authSource=poros',
        #     'username': 'poros_test', 'password': 'sGpZKsz7W1'}
        mongodb_online = {'uri': 'mongodb://%s:%s@s-2ze804aac801b914-pub.mongodb.rds.aliyuncs.com:3717/jinquan',
                        'username': 'poros_test', 'password': '6nKBKbCdBxizNRQJ'}
        uri_test = mongodb_test.get('uri') % (mongodb_test.get('username'), mongodb_test.get('password'))
        uri_online = mongodb_online.get('uri') % (mongodb_online.get('username'), mongodb_online.get('password'))
        if self.env == 'test':
            client = pymongo.MongoClient(uri_test)
            column = client['jinquan']
        elif self.env == 'online':
            client = pymongo.MongoClient(uri_online)
            column = client['poros']
        column_device = column['device_info']
        column_user = column['user_device']
        status = True
        if step == 1:
            if self.oaid or self.imei:
                if self.env == 'test':
                    env = '测试'
                elif self.env == 'online':
                    env = '线上'
                print(f'{env}数据库设备信息删除中... ')
            if self.oaid:
                device_info_query = {'oaid': self.oaid[0], 'device_id': self.oaid[1], 'app': self.oaid[2]}
                device_info = column_device.find_one(device_info_query)
                if device_info:
                    print(f"待删除设备信息数据库中已找到，信息如下：\ncolumn_name = [device_info], _id = [{device_info.get('_id')}]")
                    for _ in range(2):
                        column_device.delete_one(device_info_query)
            if self.imei:
                device_info_query = {'imei': self.imei[0], 'device_id': self.imei[1], 'app': self.imei[2]}
                device_info = column_device.find_one(device_info_query)
                if device_info:
                    print(f"待删除设备信息数据库中已找到，信息如下：\ncolumn_name = [device_info], _id = [{device_info.get('_id')}]")
                    for _ in range(2):
                        column_device.delete_one(device_info_query)
        elif step == 3:
            if self.oaid or self.imei:
                if self.env == 'test':
                    env = '测试'
                elif self.env == 'online':
                    env = '线上'
                print(f'{env}数据库校验中... ')
            if self.oaid:
                device_info_query = {'oaid': self.oaid[0], 'device_id': self.oaid[1], 'app': self.oaid[2]}
                device_info = column_device.find_one(device_info_query)
                if device_info:
                    if 'leader' in self.oaid[2] and device_info.get('client_type') == 2 or 'leader' not in \
                        self.oaid[2] \
                        and device_info.get('client_type') == 1:
                        print(f'设备信息已存入数据库中，信息如下：\ncolumn_name = [device_info], data = {device_info}')
                    else:
                        print('Client_type is error.')
                else:
                    print(f'设备信息写入数据库失败！！')
                    status = False
                user_device_query = {'user_id': self.user_id, 'device_id': self.oaid[1]}
                user_device = column_user.find_one(user_device_query)
                if user_device:
                    print(f'column_name = [user_device], data = {user_device}')
                else:
                    print(f'设备信息写入数据库失败！！')
                    status = False
            if self.imei:
                device_info_query = {'imei': self.imei[0], 'device_id': self.imei[1], 'app': self.imei[2]}
                device_info = column_device.find_one(device_info_query)
                if device_info:
                    if 'leader' in self.oaid[2] and device_info.get('client_type') == 2 or 'leader' not in \
                        self.oaid[2] \
                        and device_info.get('client_type') == 1:
                        print(f'设备信息已存入数据库中，信息如下：\ncolumn_name = [device_info], data = {device_info}')
                    else:
                        print('Client_type is error.')
                else:
                    print(f'设备信息写入数据库失败！！')
                    status = False
                user_device_query = {'user_id': self.user_id, 'device_id': self.imei[1]}
                user_device = column_user.find_one(user_device_query)
                if user_device:
                    print(f'column_name = [user_device], data = {user_device}')
                else:
                    print(f'设备信息写入数据库失败！！')
                    status = False
        return status

    def logout_prompt(self, step=2):
        print('请完成以下动作：请将账号退出登录。')
        judge_text = '2'
        judge = input(f'如果已操作完毕，请输入[{judge_text}]:')
        while judge != judge_text:
            print(f'输入错误, 请输入[{judge_text}]')
            judge = input(f'如果已操作完毕，请输入[{judge_text}]:')
        else:
            if judge == judge_text:
                return True


if __name__ == '__main__':
    lc = LogcatCathcher()
    print(' 步骤1：获取待删除设备信息 '.center(80, '='))
    lc.catch_logcat(step=1)
    if lc.check_log_file(step=1):
        if lc.check_mongo_data(step=1):
            print('\n' + ' 步骤2：账号退出登录 '.center(80, '='))
            if lc.logout_prompt(step=2):
                print('\n' + ' 步骤3：检查设备信息上传情况 '.center(80, '='))
                lc.catch_logcat(step=3)
                assert lc.check_log_file(step=3)
                assert lc.check_mongo_data(step=3)
    elif lc.online_found:  # 线上环境查询到的情况
        assert lc.check_mongo_data(step=3)
