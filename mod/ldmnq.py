# -*- coding:utf-8 -*-
import re, os, sys, threading, time, random, shutil, string, multiprocessing
from subprocess import Popen, PIPE
import uiautomator2 as u2
import mnq.func as func, mnq.app as app, mnq.mysql as mysql, mnq.api as api, mnq.telethon_func as telethon_func


# 雷电模拟器函数类
class LD(object):
    def __init__(self, ld_path, index):
        self.ld_path = ld_path
        self.ld = self.ld_path + r"\ldconsole.exe"
        self.index = str(index)
        self.share_path = '/sdcard/Pictures/'

    def run(self):
        pass

    def shell(self, cmd):
        cmd_list = [self.ld]
        if type(cmd) == list:
            cmd_list.extend(cmd)
        elif type(cmd) == str:
            cmd_list = "{} {}".format(self.ld, cmd)
        # print(cmd_list)
        _p = Popen(cmd_list, stdout=PIPE, shell=True)
        _list = _p.stdout.readlines()
        return _list

    def adb(self, cmd):
        _c = 'adb --index {} --command "{}"'.format(self.index, cmd)
        return self.shell(_c)

        # cmd=cmd.replace('shell ','')
        # return self.ldConsole(cmd)

    def ldConsole(self, cmd):
        cmd_list = '{}\ld -s {} "{}"'.format(self.ld_path, self.index, cmd)
        # print(cmd_list)
        _p = Popen(cmd_list, stdout=PIPE, shell=True)
        _list = _p.stdout.readlines()
        return _list

    # 输入文字
    def adbInputText(self, text):
        # print('输入文字',text)
        # self.adb('shell input text "{}"'.format(text))
        self.ldConsole('input text "{}"'.format(text))

    # 获取模拟器列表. 返回模拟器列表.
    def getLdList(self):
        '''获取模拟器列表. 返回模拟器列表. '''
        resp = self.shell('list2')
        dlist = []
        if resp:
            for l in resp:
                st = str(l, encoding='gbk').strip()
                if st:
                    _li = func.str2list(st, ',')
                    if _li:
                        _dic = {
                            'index': _li[0],
                            'title': _li[1],
                            'top_hwnd': _li[2],
                            'hwnd': _li[3],
                            'in_android': _li[4],
                            'pid': _li[5],
                            'vbox_pid': _li[6]
                        }
                        dlist.append(_dic)
        return dlist

    def getLdInfo(self):
        resp = self.adb('shell getprop')
        _dict = {}
        if resp:
            for l in resp:
                st = func.byte2str(l)
                if st and len(st) > 0:
                    st = st.replace('\r\n', '').strip()
                    mc = re.search(r'\[(.*)\]: \[(.*)\]', st)
                    if mc:
                        _key = mc.group(1)
                        _value = mc.group(2)
                        _dict[_key] = _value
        return _dict

    # 获取模拟器ip
    def getLdIp(self):
        resp = self.ldConsole('netcfg')
        # print(resp)
        if resp:
            for b in resp:
                st = func.byte2str(b)
                if '192.' in st:
                    mc = re.search(r'(192.*)/', st)
                    if mc:
                        ip = mc.group(1)
                        return ip

    # 运行模拟器
    def runLd(self):
        try:
            self.shell('launch --index {}'.format(self.index))
            return True
        except:
            return

    # 关闭模拟器
    def closeLd(self):
        try:
            self.shell('quit --index {}'.format(self.index))
            return True
        except:
            return

    # 新增模拟器
    def addLd(self, name):
        try:
            self.shell('add --name {}'.format(name))
            return True
        except:
            return

    # 复制模拟器
    def copyLd(self, name):
        try:
            self.shell('copy --name {} --from {}'.format(name, self.index))
            return True
        except:
            return

    # 删除模拟器
    def deleteLd(self):
        try:
            self.shell('remove  --index {}'.format(self.index))
            return True
        except:
            return

    # 修改模拟器
    def modifyLd(self, modify_str):
        '''
        修改模拟器[modify_str: 修改的模拟器参数字符. 如: --resolution 600,360,160 --cpu 1 --memory 1024 --imei auto]
        注：调用modify需要在模拟器启动前，不然可能不生效
        '''
        try:
            '''
            modify <--name mnq_name | --index mnq_idx>
            [--resolution ] // 自定义分辨率
            [--cpu <1 | 2 | 3 | 4>] // cpu设置
            [--memory <512 | 1024 | 2048 | 4096 | 8192>] // 内存设置
            [--manufacturer asus] // 手机厂商
            [--model ASUS_Z00DUO] // 手机型号
            [--pnumber 13812345678] // 手机号码
            [--imei ] // imei设置，auto就自动随机生成
            [--imsi ]
            [--simserial ]
            [--androidid ]
            [--mac ] //12位m16进制mac地址
            [--autorotate <1 | 0>]
            [--lockwindow <1 | 0>]
            '''
            'modify --index 0 --resolution 600,360,160 --cpu 1 --memory 1024 --imei auto'
            resp = self.shell('modify  --index {} {}'.format(
                self.index, modify_str))
            return resp
        except:
            return

    def ldManufacturerAndModel(self):
        '''品牌和模型'''
        dic = {}
        dic['HUAWEI'] = [
            'LIO-AN00', 'TAS-AN00', 'TAS-AL00', 'LYA-AL10', 'HMA-AL00',
            'VOG-AL00', 'ELE-AL00', 'OXF-AN10', 'OXF-AN00', 'PCT-AL10',
            'YAL-AL10', 'YAL-AL00', 'WLZ-AN00', 'SEA-AL10'
        ]
        dic['xiaomi'] = ['MI 9']
        dic['Meizu'] = ['M973Q']
        dic['smartisan'] = ['DT1901A']
        dic['OPPO'] = ['PCLM10', 'PCRT00']
        dic['vivo'] = [
            'V1916A', 'V1824A', 'V1936A', 'V1923A', 'V1938CT', 'V1938T'
        ]
        dic['samsung'] = ['SM-N9760', 'SM-N9700', 'SM-G9750', 'SM-G9730']
        dic['OnePlus'] = ['HD1910', 'HD1900', 'GM1910', 'GM1900']
        dic['blackshark'] = ['DLT-A0', 'SKW-A0']
        dic['realme'] = ['RMX1931']
        dic['nubia'] = ['NX629J', 'NX627J']
        key_list = []
        for key in dic.keys():
            key_list.append(key)
        brand = random.choice(key_list)
        model = random.choice(dic[brand])
        return brand, model

    def getRandomPhoneNumber(self):
        haoduan = ['130', '131', '132', '138', '137', '139']
        hao = random.randint(00000000, 99999999)
        number = "{}{}".format(random.choice(haoduan), hao)
        return number

    # 随机修改模拟器信息
    def randomLdInfo(self):
        brand, model = self.ldManufacturerAndModel()
        phone_number = self.getRandomPhoneNumber()
        st = "--manufacturer {} --model {} --pnumber {} --imei auto".format(
            brand, model, phone_number)
        self.modifyLd(st)

    # 重置模拟器参数并启动
    def resetLd(self):
        self.quitLd()
        time.sleep(5)
        self.randomLdInfo()
        time.sleep(1)
        self.runLd()
        for _ in range(30):
            if self.isRunning():
                return True
            time.sleep(1)

    # 备份模拟器
    def backupLd(self, file):
        try:
            self.shell('backup   --index {} --file {}'.format(
                self.index, file))
            return True
        except:
            return

    # 恢复备份
    def restoreLd(self, file):
        try:
            self.shell('restore    --index {} --file {}'.format(
                self.index, file))
            return True
        except:
            return

    # 修改名字
    def renameLd(self, name):
        try:
            self.shell('rename  --index {} --title {}'.format(
                self.index, name))
            return True
        except:
            return

    # 重启模拟器
    def rebootLd(self):
        try:
            self.shell('reboot --index {} '.format(self.index))
            return True
        except:
            return

    # 退出模拟器
    def quitLd(self):
        try:
            self.shell('quit --index {} '.format(self.index))
            return True
        except:
            return

    # 退出所有模拟器
    def quitAllLd(self):
        try:
            self.shell('quitall')
            return True
        except:
            return

    # 安装app
    def installApp(self, apk_file):
        try:
            # self.shell('installapp --index {} --filename {}'.format(index,apk_file))
            # self.adb('install {}'.format(apk_file))
            self.ldConsole('pm install {}'.format(apk_file))
            return True
        except:
            return

    # 卸载app
    def uninstallApp(self, packagename):
        try:
            self.shell('uninstallapp --index {} --packagename {}'.format(
                self.index, packagename))
            return True
        except:
            return

    # 运行app
    def runApp(self, packagename):
        '''运行app[index:模拟器坐标; packagename:应用包名]'''
        try:
            self.shell('runapp --index {} --packagename {}'.format(
                self.index, packagename))
            return True
        except:
            return

    # 退出app
    def killApp(self, packagename):
        try:
            self.shell('killapp --index {} --packagename {}'.format(
                self.index, packagename))
            return True
        except:
            return

    # 修改经纬度
    def modifyLocate(self, jd, wd):
        try:
            self.adb(
                'action --index {} --key call.locate --value {},{}'.format(
                    self.index, jd, wd))
            return True
        except:
            pass

    # 修改信息
    def setProp(self, key, value):
        try:
            self.shell('setprop --index {} --key {} --value {}'.format(
                self.index, key, value))
            return True
        except:
            pass

    # 获取信息
    def getProp(self, key):
        try:
            resp = self.shell('getprop --index {} --key {} '.format(
                self.index, key))
            return resp
        except:
            pass

    # 截图
    def screenShot(self, img):
        # img='/sdcard/Pictures/screen.jpg'
        # self.adb('shell /system/bin/screencap -p {}'.format(img))
        self.ldConsole('/system/bin/screencap -p {}'.format(img))

    # 获取硬件信息
    def getDeviceInfo(self):
        info = {}
        info['imei'] = func.byte2str(
            self.ldConsole('getprop phone.imei')[0]).strip()
        info['simserial'] = func.byte2str(
            self.ldConsole('getprop phone.simserial')[0]).strip()
        info['androidid'] = func.byte2str(
            self.ldConsole('getprop phone.androidid')[0]).strip()
        info['manufacturer'] = func.byte2str(
            self.ldConsole('getprop phone.manufacturer')[0]).strip()
        info['model'] = func.byte2str(
            self.ldConsole('getprop phone.model')[0]).strip()
        info['pnumber'] = func.byte2str(
            self.ldConsole('getprop phone.number')[0]).strip()
        info['imsi'] = func.byte2str(
            self.ldConsole('getprop phone.imsi')[0]).strip()
        info['net_operatorname'] = func.byte2str(
            self.ldConsole('getprop phone.net_operatorname')[0]).strip()
        info['sim_country'] = func.byte2str(
            self.ldConsole('getprop phone.sim_country')[0]).strip()
        info['ro.product.board'] = func.byte2str(
            self.ldConsole('getprop ro.product.board')[0]).strip()
        info['ro.product.brand'] = func.byte2str(
            self.ldConsole('getprop ro.product.brand')[0]).strip()
        info['ro.serialno'] = func.byte2str(
            self.ldConsole('getprop ro.serialno')[0]).strip()
        info['ro.build.host'] = func.byte2str(
            self.ldConsole('getprop ro.build.host')[0]).strip()
        info['ro.product.name'] = func.byte2str(
            self.ldConsole('getprop ro.product.name')[0]).strip()
        info['ro.product.device'] = func.byte2str(
            self.ldConsole('getprop ro.product.device')[0]).strip()
        info['ro.product.board'] = func.byte2str(
            self.ldConsole('getprop ro.product.board')[0]).strip()
        info['dhcp.eth0.ipaddress'] = func.byte2str(
            self.ldConsole('getprop dhcp.eth0.ipaddress')[0]).strip()
        info['ro.build.id'] = func.byte2str(
            self.ldConsole('getprop ro.build.id')[0]).strip()
        return info

    # 随机重置模拟器硬件信息
    def resetDeviceInfo(self):
        brand, model = self.ldManufacturerAndModel()
        info = {}
        info['imei'] = ''.join(random.choice(string.digits) for _ in range(15))
        info['simserial'] = ''.join(
            random.choice(string.digits) for _ in range(20))
        info['androidid'] = ''.join(
            random.choice(string.digits + string.ascii_lowercase)
            for _ in range(16))
        info['manufacturer'] = brand
        info['model'] = model
        info['pnumber'] = ''.join(
            random.choice(string.digits) for _ in range(11))
        info['imsi'] = ''.join(random.choice(string.digits) for _ in range(15))
        us_mobile_operator_list = [
            'AT&T', 'Boost', 'Altice Mobile', 'Nemont CDMA', 'T-Mobile',
            'Union Telephone', 'Verizon'
        ]
        info['net_operatorname'] = random.choice(us_mobile_operator_list)
        info['sim_country'] = 'us'
        info['ro.product.board'] = model
        info['ro.product.brand'] = brand
        info['ro.serialno'] = ''.join(
            random.choice(string.digits + string.ascii_lowercase)
            for _ in range(8))
        info['ro.build.host'] = brand
        info['ro.product.name'] = model
        info['ro.product.device'] = brand
        info['ro.build.id'] = ''.join(
            random.choice(string.digits + string.ascii_uppercase)
            for _ in range(6))

        for k, v in info.items():
            if not '.' in k:
                console = 'phone.{}'.format(k)
                console = 'setprop {} {}'.format(console, v)
                print(k, console)
                resp = self.ldConsole(console)
                print(resp)

        pass

    # 获取所有app列表
    def getAppList(self):
        '''获取已安装app列表[index:模拟器坐标][返回:list]'''
        try:
            app_list = []
            # resp=self.adb('shell pm list packages')
            resp = self.ldConsole('pm list packages')
            if resp:
                for l in resp:
                    st = func.byte2str(l).strip().replace('package:', '')
                    if st and len(st) > 0:
                        app_list.append(st)
            return app_list
        except:
            pass

    # 安装atx_agent服务 注意: 确保atx_agent文件在当前目录
    def installAtxAgent(self):
        '''安装atx服务[index:模拟器坐标][返回:list]'''
        print('开始安装atx服务')
        file = 'atx-agent'
        if os.path.exists(file):
            # self.adb('push atx-agent /data/local/tmp')
            # self.adb('shell chmod 755 /data/local/tmp/atx-agent')
            # self.adb('shell /data/local/tmp/atx-agent server -d')
            self.ldConsole('cp {}atx-agent /data/local/tmp/atx-agent'.format(
                self.share_path))
            self.ldConsole('chmod 755 /data/local/tmp/atx-agent')
            self.ldConsole('/data/local/tmp/atx-agent server -d')
            # self.run_atx()
            return True
        else:
            print('atx-agent不存在')

    def installApps(self):
        '''安装初始app[index:模拟器坐标][返回:True]'''
        # 安装Telegram.apk,app-uiautomator.apk,clipper.apk

        app_list = self.getAppList()
        # 安装u2
        if 'com.github.uiautomator' not in app_list:
            self.installAtxAgent()
            print("安装u2插件")
            if os.path.exists('app-uiautomator.apk'):
                self.installApp('{}app-uiautomator.apk'.format(
                    self.share_path))
        # 安装telegram
        if 'org.telegram.messenger' not in app_list:
            print('安装telegram')
            self.installApp('{}Telegram.apk'.format(self.share_path))

        return True

    # 启动atx服务
    def runAtx(self):
        '''运行atx服务(自动安装)[index:模拟器坐标][返回:True]'''
        # resp=self.adb('shell /data/local/tmp/atx-agent server -d')
        resp = self.ldConsole('/data/local/tmp/atx-agent server -d')
        for l in resp:
            l = func.byte2str(l)
            # print('atx服务:',self.index,l)
            if 'not found' in l:
                if self.installAtxAgent():
                    return True
        return True

    # 判断模拟器是否已经运行
    def isRunning(self):
        '''模拟器是否运行并已经进入安卓系统'''
        ld_list = self.getLdList()
        if ld_list:
            for dic in ld_list:
                index = dic['index']
                if index == self.index:
                    if dic['in_android'] == '1':
                        return True
        return


# 雷电的任务类
def TgRegFunc(config_dict, que, rlock):
    tgreg_class = TelegramRegClass(config_dict, que, rlock)
    tgreg_class.run()


# class TelegramRegClass(threading.Thread):
class TelegramRegClass(object):
    def __init__(self, config_dict, que, rlock):
        super(TelegramRegClass, self).__init__()
        self.config_dict = config_dict
        self.dbfile = self.config_dict['dbfile']
        self.sql_class = mysql.MySqlite(self.dbfile)
        self.que = que
        self.rlock = rlock
        self.ld_path = self.config_dict['ld_path']
        self.live_dbfile = 'db/live.db'
        self.stop_thread = False

        self.ld = None
        self.index = None
        self.ld_ip = None

        # self.index=None
        # self.ld=LD(self.ld_path,self.index)

    def run(self):
        '''
        启动指定数量的模拟器
        判断模拟器是否安装了telegram, uiautomator2, clipboard等必装app, 没有则进行安装

        '''
        try:
            # 获取模拟器
            sql = "select * from account where status=1 limit 1"
            with self.rlock:
                sql_data = mysql.MySqlite(self.live_dbfile).select(sql)
                if sql_data:
                    self.ld_title = sql_data[0]['task']
                    self.index = sql_data[0]['type']
                    self.ld_ip = sql_data[0]['proxy']
                    mysql.MySqlite(self.live_dbfile).ui(
                        "update account set status=2 where type={}".format(
                            self.index))

            # 开始执行
            if self.index and self.ld_ip:
                # 模拟器实例
                self.ld = LD(self.ld_path, self.index)

                # 初始化模拟器,包括:安装并启动atx服务和相关app
                self.print_msg(self.ld_title, '初始化')
                self.initLd()
                # telegram操作实例
                self.tg = app.Telegram(self.ld_ip, self.ld)

                # 主任务函数
                while True:
                    if self.stop_thread:
                        return True
                    # 判断注册任务是否完成
                    sql = "select count(id) as count from account where status=1"
                    sql_data = self.sql_class.select(sql)
                    if sql_data:
                        reg_num = sql_data[0]['count']
                        self.print_msg('已注册{}'.format(reg_num))
                        if reg_num >= self.config_dict['reg_count']:
                            self.print_msg(self.ld_title, '注册任务已完成')
                            return True
                    try:
                        self.main()
                    except Exception as e:
                        func.err_log("TelegramRegClass-main:{}".format(str(e)))
        except Exception as e:
            func.err_log('telegramReg:{}'.format(str(e)))
        finally:
            if self.index:
                with self.rlock:
                    mysql.MySqlite(self.live_dbfile).ui(
                        "update account set status=1 where type={}".format(
                            self.index))
            pass

    def main(self):
        # print(self.config_dict)
        '''
        获取模拟器
        初始化模拟器(安装atx, telegram等)
        获取代理
        模拟器设置代理
        获取号码
        模拟器登陆
        teleton 注册
        模拟器获取验证码
        telethon输入验证码
        获取session
        '''
        self.tdict = {}  # 临时table, 用于存放各个步骤获取的数据
        self.tgfile, self.sql_id, self.session = None, None, None
        self.proxy_str = ""
        self.api_id, self.api_hash, self.first_name, self.last_name = None, None, None, None
        self.user_id, self.account_id = None, None
        self.pid, self.hwnd = None, None
        self.vcode = None
        self.task_status = False

        self.device_dict = None
        try:
            # 获取号码
            self.print_msg('开始获取号码')
            self.country, self.phone = self.get_phone()
            if self.country and self.phone:
                with self.rlock:  # 更新模拟器的使用次数, 如果超过单机值, 则随机模拟器参数并重启
                    mysql.MySqlite('db/live.db').ui(
                        "update account set use_num=use_num+1 where type={}".
                        format(self.index))
                self.full_phone = '+' + self.country + self.phone
                self.print_msg(self.ld_title, '号码:', self.full_phone)
                # 启动telegram
                self.print_msg(self.ld_title, '启动Telegram')
                # self.tg.startTg()
                self.print_msg(self.ld_title, '号码:', self.full_phone, '开始设置参数')
                yybl = app.YYBL(self.ld_ip, self.ld)
                yybl.startApp()  # 启动应用变量
                self.device_dict = yybl.startTelegram(
                    self.full_phone)  # 从应用变量中设置参数并启动telegram
                time.sleep(3)
                self.tg.startApp()  # 启动telegram注册程序
                if self.config_dict['proxy']:
                    # 获取ip
                    set_proxy = False
                    for _ in range(5):
                        self.proxy_str = self.get_proxy()
                        self.print_msg(self.ld_title, '代理ip:', self.proxy_str)

                        if self.proxy_str:
                            mc = re.search(r'//(.*):(.*)', self.proxy_str)
                            if mc:
                                proxy_ip = mc.group(1)
                                port = mc.group(2)
                                # print(proxy_ip,port)
                                # 设置telegram代理ip
                                if self.tg.setProxy(proxy_ip, port):
                                    set_proxy = True
                                    self.print_msg(self.ld_title, '代理设置成功')
                                    break
                    if not set_proxy:
                        self.print_msg(self.ld_title, '设置代理失败')
                        return

                # 获取昵称
                self.first_name, self.last_name = self.get_nickname()
                self.print_msg(self.ld_title, self.full_phone, '昵称:',
                               self.first_name, self.last_name)
                # 输入手机号码
                self.print_msg(self.ld_title, self.full_phone, '输入手机号码')
                if self.tg.inputPhone(self.country, self.phone):
                    self.print_msg(self.ld_title, self.full_phone, '开始获取验证码')
                    code = self.get_code()
                    if code:
                        self.print_msg(self.ld_title, self.full_phone,
                                       '开始输入验证码')
                        if self.tg.inputCode(code):
                            self.print_msg(self.ld_title, self.full_phone,
                                           '输入验证码{}成功'.format(code))
                            self.print_msg(self.ld_title, self.full_phone,
                                           '开始输入昵称:')
                            self.tg.inputNickname(self.first_name,
                                                  self.last_name)
                else:
                    self.print_msg(self.ld_title, self.full_phone, '注册/号码异常')
                    return
            else:
                self.print_msg(self.ld_title, '无可用帐号')
                self.stop_thread = True
                return
            if self.tg.isIndexPage():
                self.print_msg(self.ld_title, self.full_phone, 'APP注册成功:')
                time.sleep(1)
                sql = 'update account set status=1 where id={}'.format(
                    self.account_id)
                self.sql_class.ui(sql)
                try:
                    # 设置随机用户名
                    if self.config_dict['random_username']:
                        self.print_msg(self.ld_title, self.full_phone, '设置昵称')
                        username = self.tg.setUsername()
                        if username:
                            sql = "update account set username='{}' where id={}".format(
                                username, self.account_id)
                            self.sql_class.ui(sql)
                    # 上传头像
                    if self.config_dict['upload_avatar']:
                        self.print_msg(self.ld_title, self.full_phone, '上传头像')
                        # 复制图片到模拟器 ( 更改md5 )
                        avatar_img = self.copyAvatar().replace('\\', '/')
                        time.sleep(1)
                        # 上传头像图片
                        self.tg.uploadAvatar(avatar_img)
                        # 删除头像图片
                        self.ld.ldConsole('rm {}'.format(avatar_img))
                    # 随机建群
                    if self.config_dict['create_group']:
                        ''.join(
                            random.choice(string.digits) for _ in range(15))
                        channel_name = ''.join(
                            random.choice(string.ascii_lowercase)
                            for _ in range(7))
                        invite_username = 'wuya88bot'
                        sql = "select username from account where length(username)>0 and id!={} order by random() limit 1".format(
                            self.account_id)
                        sql_data = self.sql_class.select(sql)
                        if sql_data:
                            invite_username = sql_data[0]['username']

                        self.tg.createChannel(channel_name, invite_username)
                    # 备份
                    self.print_msg(self.ld_title, self.full_phone, '开始备份')
                    self.ld.killApp('org.telegram.messenger')  # 关闭telegram
                    # Tai备份文件
                    tai = app.Tai(self.ld_ip, self.ld)
                    tai.startTai()
                    if tai.backupApp("Telegram"):
                        self.moveBakcupFile()
                    self.ld.killApp(tai.packagename)
                except Exception as e:
                    self.print_msg(self.ld_title, self.full_phone, str(e))
                finally:
                    return True

        except Exception as e:
            self.print_msg(self.ld_title, self.full_phone, str(e))
        finally:
            # # 释放号码
            # self.release_phone()
            pass
            # # 关闭客户端
            # if self.pid and self.hwnd:
            #     self.print_msg(self.full_phone,'关闭客户端')
            #     self.tg.close_client(self.tgfile)

    # 初始化模拟器,
    def initLd(self):
        '''初始化模拟器,包括:安装并启动atx服务和相关app'''
        self.ld.installApps()
        self.ld.runAtx()
        pass

    # 随机获取头像图片文件
    def get_avatar_img(self, folder):
        '''随机获取头像图片文件'''
        img_list = []
        if os.path.exists(folder) and os.path.isdir(folder):
            flist = os.listdir(folder)
            for f in flist:
                if '.jpg' in f or '.png' in flist:
                    img_list.append(f)
            if img_list:
                img = random.choice(img_list)
                if img:
                    img = os.path.join(folder, img)
                    _tmp_img = func.copy_tmp_img(img)
                    if _tmp_img:
                        return _tmp_img

    # 从目录随机复制图片到模拟器中(并广播), 用于图片上传
    def copyAvatar(self):
        source_dir = self.config_dict['avatar']
        pc_share = self.config_dict['pc_share']
        ld_share = self.config_dict['ld_share']
        tmp_img = self.get_avatar_img(source_dir)  # 获取随机图片
        img_name = os.path.basename(tmp_img)
        # print(img_name)
        if tmp_img:
            pass
            # 将随机图片复制到模拟器电脑共享目录下
            pc_share_img = os.path.join(pc_share, img_name)
            # print('pc_share_img',pc_share_img)
            shutil.move(tmp_img, pc_share_img)
            if os.path.exists(pc_share_img):
                # 广播刷新图库
                resp = self.ld.ldConsole(
                    'am broadcast -a android.intent.action.MEDIA_MOUNTED -d file://{}'
                    .format(ld_share))
                # print(resp)
                ld_share_img = os.path.join(ld_share, img_name)
                # print(ld_share_img)
                return ld_share_img

    # 备份文件移动到共享目录
    def moveBakcupFile(self):
        ld_share = self.config_dict['ld_share']
        # index=self.index
        index = 'Tai'
        phone = self.full_phone
        app_dir = '/storage/emulated/legacy/TitaniumBackup'
        files = self.ld.ldConsole('ls {}'.format(app_dir))
        if files:
            # 创建目录
            _dir = os.path.join(self.config_dict['pc_share'], index, phone)
            if not os.path.exists(_dir):
                os.makedirs(_dir)
            for f in files:
                f = func.byte2str(f).strip()
                if f:
                    source_file = os.path.join(app_dir, f).replace('\\', '/')
                    target_file = os.path.join(ld_share, index, phone,
                                               f).replace('\\', '/')

                    # 复制操作
                    # print(source_file,target_file)
                    resp = self.ld.ldConsole('mv {} {}'.format(
                        source_file, target_file))
                    # print(resp)
            # 保存硬件信息
            if self.device_dict:
                txt = os.path.join(_dir, 'info.txt')
                info = [str(self.device_dict)]
                func.write_list_txt(txt, info)

    def print_msg(self, *args):
        '''
        打印日志到UI界面
        '''
        m = " "
        if args:
            m = m.join([str(x) for x in args])
        # self.mdict['msg']=m
        try:
            self.que.put(m)
        except:
            pass

    def get_phone(self):
        '''获取号码  []返回[country:国码; phone: 电话号码; tid: api记录id,用于释放]'''
        country = None
        phone = None
        # 海外1 sms-activate.ru
        if self.config_dict['platform'] == "海外1":
            if "|" in self.config_dict['country']:
                mc = re.search(r'(.*?)\|(.*)', self.config_dict['country'])
                if mc:
                    country_id = mc.group(1)
                    country = mc.group(2)
                for _ in range(3):
                    res = api.Sms_activate_Phone(self.config_dict['token'],
                                                 country=country_id)
                    # print(res)
                    if res:
                        phone = res['phone']
                        phone = phone[len(country):]
                        self.tdict['tid'] = res['tid']
                        # self.account_id=mysql.SqliteInsert("insert into account (status,type,task,country,phone) values (0,'haiwai1','reg_class','%s','%s') " % (country,phone),self.dbfile)
                        self.account_id = mysql.MySqlite(self.dbfile).insert(
                            "insert into account (status,type,task,country,phone) values (0,'haiwai1','reg_class','%s','%s') "
                            % (country, phone))
                        # print(country,phone)
                        return country, phone
                    else:
                        self.print_msg('请求号码失败')

        # 专属1 平台
        elif self.config_dict['platform'] == '专属1':  # 专属1
            country, phone = None, None
            # 获取country
            custom_platform_options = self.config_dict[
                'custom_platform_options']
            mc = re.search(r"(.*?)\|(.*)", custom_platform_options)
            if mc:
                country = mc.group(1)
            self.tdict['phone_url'] = mc.group(2)
            # 获取phone
            with self.rlock:
                if self.config_dict['loop']:  # 循环
                    sql = "select * from account where status!=1 and type='private_account'  and task='reg_class' order by use_num asc limit 1"
                else:  # 不循环
                    sql = "select * from account where status=0 and type='private_account'  and task='reg_class' and use_num=0 order by use_num asc limit 1"
                sql_data = self.sql_class.select(sql)
                if sql_data:
                    self.account_id = sql_data[0]['id']
                    phone = sql_data[0]['phone']
                    token_str = sql_data[0]['content']
                    self.tdict['phone_token'] = token_str

                    self.sql_class.ui(
                        "update account set use_num=use_num+1 where id={}".
                        format(self.account_id))
                if phone and country:
                    return country, phone

        elif self.config_dict['platform'] == '5sim':
            country, phone = None, None
            if self.config_dict['country'] and "|" in self.config_dict[
                    'country']:
                mc = re.search(r'(.*?)\|(.*)', self.config_dict['country'])
                if mc:
                    country_id = mc.group(1)
                    country = mc.group(2)
                token = self.config_dict['token']
                for _ in range(3):
                    rdict = api.FiveSimClass(token).get_phone(country_id)
                    if rdict:
                        self.tdict['tid'] = rdict['id']
                        phone = rdict['phone']
                        if phone:
                            phone = phone.replace('+', '')
                            phone = phone[len(country):]
                            self.account_id = mysql.MySqlite(
                                self.dbfile
                            ).insert(
                                "insert into account (status,type,task,country,phone) values (0,'5sim','reg_class','%s','%s') "
                                % (country, phone))
                            return country, phone
                        else:
                            self.print_msg('请求号码失败')
        elif self.config_dict['platform'] == '柠檬':
            mc = re.search(r'(.*?)\|(.*)', self.config_dict['country'])
            if mc:
                country_id = mc.group(1)
                country = mc.group(2)
            username = self.config_dict['username']
            password = self.config_dict['password']
            for _ in range(3):
                rdict = api.NmgjClass(username, password).get_phone(country_id)
                if rdict:
                    phone = rdict['data']
                    phone = phone.replace('+', '')
                    phone = phone[len(country):]
                    self.account_id = mysql.MySqlite(self.dbfile).insert(
                        "insert into account (status,type,task,country,phone) values (0,'nmgj','reg_class','%s','%s') "
                        % (country, phone))
                    if country and phone:
                        return country, phone
                    else:
                        self.print_msg('请求号码失败')
        return None, None

    def get_api_in_sql(self):
        # 从数据库中获取, 如果没有则随机有效信息
        sql = "select * from account where api_id is not null and api_hash is not null and length(api_id)>5 and length(api_hash)>10 order by random() limit 1"
        tmp_data = mysql.SqliteSelect(sql, self.dbfile)
        if tmp_data and len(tmp_data) > 0 and len(
                tmp_data[0]['api_id']) > 5 and len(
                    tmp_data[0]['api_hash']) > 10:
            api_id = tmp_data[0]['api_id']
            api_hash = tmp_data[0]['api_hash']
        else:
            api_list = [['1822649', '6be76876b84a8149ece1c418524a3cc6'],
                        ['1978922', '988734fe7f8a912b94f046b48c6dd932'],
                        ['1861739', '2be21bcc603cde584ee8896e5272914e'],
                        ['1951154', '5ae880d8b7d6f9b83a1113dd09db1106'],
                        ['1504261', 'f3b966835bc67cbfd8155e275fd49b07'],
                        ['2347264', '26c48259bd538fd53fe41bc91155fb6c'],
                        ['2516785', '2b098f1e75c471d39fbe3dc923789bc6'],
                        ['2869586', '4188b2a4515b3c86b080392c53e7f40f'],
                        ['2006874', '44db0882f8d1ffd433b86d31fd7065fd'],
                        ['2159791', '5d89b723204e8c8fcaf36cf1278599d0'],
                        ['2899996', '811c8e6e1c4667d8030898214146ccc6'],
                        ['2370942', '928c08af9f4f0803679de643b6c668d7'],
                        ['2561072', '982c1c5f8a17eb531107d368a7f95ec1'],
                        ['2179088', '9889e2eec5f24056f8dd4d0c4ad050b1'],
                        ['2432202', '9e2ec24bf651b7041880302f6190dd86'],
                        ['2477971', 'b4db23aff65c3a9d0d70a08ea7c29922'],
                        ['2559656', 'd08b2470b6f72cc44c6266ebcb41a0d7'],
                        ['2734493', 'dd985add75e91fe4389ae36f792454b2'],
                        ['2079217', 'e1ed7b324ee08641993c08a1d039f6e2'],
                        ['2385812', 'e219d8985bee383421bf83e97116052a'],
                        ['2664742', 'f7bd02dd2af17eac6b6dd0e1d62e6895']]
            api_info = random.choice(api_list)
            api_id = api_info[0]
            api_hash = api_info[1]
        return api_id, api_hash

    def release_phone(self):
        '''释放号码'''
        if self.config_dict['platform'] == "海外1" and self.phone:
            self.print_msg(self.phone, '释放号码')
            if self.session:
                if 'tid' in self.tdict.keys():
                    api.Sms_activate_SetStatus(
                        '6', self.tdict['tid'],
                        self.config_dict['token'])  # 通知已经激活
            else:
                if 'tid' in self.tdict.keys():
                    api.Sms_activate_SetStatus(
                        '8', self.tdict['tid'],
                        self.config_dict['token'])  # 未激活成功, 取消号码
        elif self.config_dict['platform'] == '5sim':
            token = self.config_dict['token']
            oid = self.tdict['tid']
            if self.session:
                api.FiveSimClass(token).finish_order(oid)
            else:
                api.FiveSimClass(token).ban_order(oid)
        elif self.config_dict['platform'] == '柠檬':
            username = self.config_dict['username']
            password = self.config_dict['password']
            api.NmgjClass(username, password).ban_number(self.full_phone)

    def get_proxy(self):
        '''获取代理ip'''
        sql = "select * from proxy where status=1 order by random() limit 1"
        sql_data = mysql.SqliteSelect(sql, 'db/proxy.db')
        if sql_data:
            proxy_str = sql_data[0]['proxy_str']
            return proxy_str
        else:
            return ""

    def spam_bot(self):
        log_dict = {}
        log_dict['task'] = 'spam_bot'
        log_dict['target'] = 'me'
        log_dict['phone'] = "+" + self.country + self.phone
        log_dict['session'] = self.session
        log_dict['proxy_str'] = self.proxy_str
        log_dict['from_id'] = '777000'
        log_dict['dbfile'] = self.config_dict['dbfile']
        tgf = telethon_func.TelethonFunc(log_dict)
        result_dict = tgf.run()
        if result_dict['status']:
            return True

    # 上传头像
    def upload_avatar(self):
        # 随机获取头像图片文件
        def get_avatar(folder):
            '''随机获取头像图片文件'''
            img_list = []
            if os.path.exists(folder) and os.path.isdir(folder):
                flist = os.listdir(folder)
                for f in flist:
                    if '.jpg' in f or '.png' in flist:
                        img_list.append(f)
                if img_list:
                    img = random.choice(img_list)
                    if img:
                        img = os.path.join(folder, img)
                        _tmp_img = func.copy_tmp_img(img)
                        if _tmp_img:
                            return _tmp_img

        self.print_msg(self.full_phone, '开始上传头像')
        log_dict = {}
        log_dict['task'] = 'upload_avatar'
        log_dict['phone'] = "+" + self.country + self.phone
        log_dict['target'] = 'me'
        log_dict['session'] = self.session
        log_dict['proxy_str'] = self.proxy_str
        log_dict['dbfile'] = self.config_dict['dbfile']
        log_dict['img_file'] = get_avatar(self.config_dict['avatar'])
        # print(log_dict)
        tgf = telethon_func.TelethonFunc(log_dict)
        result_dict = tgf.run()
        self.print_msg(log_dict['phone'], result_dict['resp'])

        # print(result_dict)
        # print('================================================')

    # 随机建群
    def create_group(self):
        self.print_msg(self.full_phone, '开始随机建群')
        log_dict = {}
        log_dict['task'] = 'create_group'
        log_dict['phone'] = "+" + self.country + self.phone
        log_dict['target'] = 'me'
        log_dict['session'] = self.session
        log_dict['proxy_str'] = self.proxy_str
        log_dict['dbfile'] = self.config_dict['dbfile']

        log_dict['title'] = func.GBK2312(random.randint(1, 5))
        log_dict['about'] = func.GBK2312(random.randint(5, 10))
        # print(log_dict)
        tgf = telethon_func.TelethonFunc(log_dict)
        result_dict = tgf.run()
        self.print_msg(log_dict['phone'], result_dict['resp'])
        # print(result_dict)
        # print('================================================')

    # 设置随机用户名
    def set_random_username(self):
        self.print_msg(self.full_phone, '开始设置用户名')
        log_dict = {}
        log_dict['task'] = 'set_username'
        log_dict['phone'] = "+" + self.country + self.phone
        log_dict['target'] = 'me'
        log_dict['proxy_str'] = self.proxy_str
        log_dict['session'] = self.session
        log_dict['dbfile'] = self.config_dict['dbfile']
        # print(log_dict)
        tgf = telethon_func.TelethonFunc(log_dict)
        result_dict = tgf.run()
        self.print_msg(log_dict['phone'], result_dict['resp'])
        # print(result_dict)
        # print('================================================')

    # 设置密码
    def set_password(self):
        self.print_msg(self.full_phone, '开始设置密码')
        log_dict = {}
        log_dict['task'] = 'set_password'
        log_dict['phone'] = "+" + self.country + self.phone
        log_dict['target'] = 'me'
        log_dict['proxy_str'] = self.proxy_str
        log_dict['session'] = self.session
        log_dict['dbfile'] = self.config_dict['dbfile']
        log_dict['account_id'] = self.account_id
        log_dict['password'] = "{}_{}".format('wuya88.com', func.RandomStr(7))
        # print(log_dict)
        tgf = telethon_func.TelethonFunc(log_dict)
        result_dict = tgf.run()
        if result_dict['status']:  # 修改成功
            # 更新密码到表
            with self.rlock:
                _sql = "update account set password='{}' where id={} ".format(
                    log_dict['password'], self.account_id)
                self.sql_class.ui(_sql)
        self.print_msg(log_dict['phone'], result_dict['resp'])
        # print(result_dict)
        # print('================================================')

    def get_nickname(self):
        '''获取昵称[]返回:[first_name; last_name]'''
        if self.config_dict['random_nickame']:  # 随机昵称
            first_name = func.GBK2312(1)
            first_name = func.cn2py(first_name)
            last_name = func.GBK2312(1)
            last_name = func.cn2py(last_name)
            return first_name, last_name
        else:  # 列表中取昵称
            sql = "select * from content where type='nickname' order by random() limit 1"
            # sql_data=mysql.SqliteSelect(sql,self.dbfile)
            sql_data = self.sql_class.select(sql)
            if sql_data:
                nickname_str = sql_data[0]['content']
                if nickname_str:
                    mc = re.search(r'(.*?)\|(.*)', nickname_str)
                    if mc:
                        first_name = mc.group(1)
                        last_name = mc.group(2)
                    else:
                        first_name = nickname_str[0:int(len(nickname_str) / 2)]
                        last_name = nickname_str[int(len(nickname_str) /
                                                     2):len(nickname_str)]
                    return first_name, last_name

    #     return sql_id
    def get_session(self, log_dict):
        '''获取session字符[sql_id:数据库id]返回[true/fasle ,session 字符串存储到数据库和txt中]'''
        tgf = telethon_func.TelethonFunc(log_dict, None, self.getCodeInLd)
        result_dict = tgf.get_session()
        return result_dict

    def getCodeInLd(self):
        '''从模拟器app中获取验证码'''
        self.tg.searchKeyword('Telegram')
        code = self.tg.getLoginCode()
        return code

    def get_code(self):
        '''
        获取手机验证码
        '''
        try:
            self.print_msg(self.full_phone, '正在获取验证码. 请稍后...')
            if self.config_dict['platform'] == '海外1':  # 国外1
                code = api.Sms_activate_GetStatus(self.phone,
                                                  self.tdict['tid'],
                                                  self.config_dict['token'])
            elif self.config_dict['platform'] == '专属1':  # 专属1
                custom_platform_options = self.config_dict[
                    'custom_platform_options']
                mc = re.search(r"(.*?)\|(.*)", custom_platform_options)
                self.config_dict['country'] = mc.group(1)
                self.config_dict['phone_url'] = mc.group(2)
                code = api.Private1_GetCode(url=self.tdict['phone_url'],
                                            token=self.tdict['phone_token'],
                                            phone=self.phone)
            elif self.config_dict['platform'] == '5sim':
                if 'tid' in self.tdict and self.tdict['tid']:
                    token = self.config_dict['token']
                    oid = self.tdict['tid']
                    code = api.FiveSimClass(token).get_code(oid)
            elif self.config_dict['platform'] == '柠檬':
                username = self.config_dict['username']
                password = self.config_dict['password']
                code = api.NmgjClass(username,
                                     password).get_code(self.full_phone)
            if code:
                self.print_msg(self.full_phone, '获取到验证码:', code)
                return code
            else:
                self.print_msg(self.full_phone, '验证码获取失败')
                return
        except Exception as e:
            func.err_log("get_code:" + str(e))

    def get_api(self):
        '''获取api信息'''
        try:
            random_hash = api.MyTelegramOrg_SendPassword(
                self.country, self.phone, self.proxy_str)
            # print(random_hash)
            if random_hash:
                log_dict = {}
                log_dict['task'] = 'get_msg'
                log_dict['target'] = 'me'
                log_dict['phone'] = "+" + self.country + self.phone
                log_dict['session'] = self.session
                log_dict['proxy_str'] = self.proxy_str
                log_dict['from_id'] = '777000'
                log_dict['dbfile'] = self.config_dict['dbfile']
                tgf = telethon_func.TelethonFunc(log_dict)
                result_dict = tgf.run()
                if result_dict['status']:
                    msg = result_dict['resp']
                    # print(msg)
                    # 匹配验证码
                    if msg and 'my.telegram.org' in msg:
                        mc = re.search(
                            r'my.telegram.org.*?[,|:]([\s\S]*?)\s\s',
                            msg)  # 匹配
                        if not mc:
                            mc = re.search(r'([a-zA-Z0-9]*?\-.*)', msg)  #
                        if mc:
                            web_login_code = mc.group(1)
                            # 获取登陆后的cookie字典
                            if web_login_code:
                                # print('web_login_code',web_login_code)
                                cookie_dict = api.MyTelegramOrg_Login(
                                    self.country, self.phone, random_hash,
                                    web_login_code, self.proxy_str)
                                if cookie_dict:
                                    cookie = "stel_token=" + cookie_dict[
                                        'stel_token']
                                    res_dict = api.MyTelegramOrg_App(
                                        self.phone, cookie,
                                        self.proxy_str)  # 获取api_id api_hash
                                    # print(res_dict)
                                    if res_dict:
                                        # print(res_dict)
                                        sql = "update account set api_id='%s',api_hash='%s' where id=%s" % (
                                            res_dict['api_id'],
                                            res_dict['api_hash'],
                                            self.account_id)
                                        # mysql.SqliteUI(sql,self.dbfile)
                                        self.sql_class.ui(sql)
                                        self.print_msg(self.full_phone,
                                                       'api信息设置成功')
                                        return True
        except Exception as e:
            func.err_log("get_api:" + str(e))

    def copy_client(self):
        '''
        复制客户端到指定目录
        '''
        phone_dir = "%s-%s" % (self.country, self.phone)
        source_file = self.config_dict['tgfile']
        target_dir = self.config_dict['savepath'] + '\\' + phone_dir
        target_file = target_dir + r'\Telegram.exe'

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)  # 新建文件夹
        if not os.path.exists(target_file):
            self.print_msg(self.full_phone, '复制客户端')
            shutil.copyfile(source_file, target_file)  # 复制文件到新目录
        if os.path.exists(target_file):
            return target_file

    def get_telethon_code(self):
        '''
        通过telethon获取登陆验证码
        '''
        log_dict = {}
        log_dict['task'] = 'get_msg'
        log_dict['target'] = 'me'
        log_dict['phone'] = "+" + self.country + self.phone
        log_dict['session'] = self.session
        log_dict['proxy_str'] = self.proxy_str
        log_dict['from_id'] = '777000'
        log_dict['dbfile'] = self.config_dict['dbfile']
        tgf = telethon_func.TelethonFunc(log_dict)
        result_dict = tgf.run()
        if result_dict['status']:
            msg = result_dict['resp']
            if msg and 'Login code' in msg:
                mc = re.search(r'\d{5,}', msg)
                if mc:
                    vcode = mc.group(0)
                    return vcode

    def login_client(self):
        '''
        登陆客户端 []返回:[true/else]
        '''
        self.print_msg(self.full_phone, '开始登陆客户端')
        self.tg = TgClass()  # 初始化tg客户端类
        # 复制并启动客户端
        self.tgfile = self.copy_client()
        if self.tgfile:
            self.print_msg(self.full_phone, '启动客户端')
            self.pid, self.hwnd = self.tg.start_client(self.tgfile,
                                                       random_screen=False)
            # 设置代理ip
            if self.pid and self.hwnd and self.config_dict['proxy']:
                self.print_msg(self.full_phone, '开始设置代理ip')
                for _ in range(2):
                    proxy_status = self.tg.set_proxy(self.hwnd, self.proxy_str)
                    if proxy_status:
                        self.print_msg(self.full_phone, '代理设置成功')
                        break
                    else:
                        return

        # 登陆
        self.print_msg(self.full_phone, '开始登陆')
        # 输入号码
        # print(self.hwnd,self.country,self.phone)
        login_status = self.tg.input_phone(self.hwnd, self.country, self.phone)
        # print(login_status)
        if login_status == 'success':
            # 收取/填写验证码
            self.print_msg(self.full_phone, '获取验证码')
            login_code = self.get_telethon_code()
            if login_code:
                self.print_msg(self.full_phone, '验证码:', login_code)
                self.tg.input_vcode(self.hwnd, login_code)
                # 填写昵称
                self.print_msg(self.full_phone, '填写昵称')
                if self.tg.input_nickname(self.hwnd, self.first_name,
                                          self.last_name):
                    self.print_msg(self.full_phone, '客户端登陆成功')
                    time.sleep(10)
                    return True
            # 获取验证码
        elif login_status == 'banned':
            self.print_msg(self.full_phone, '号码被屏蔽')
            return
        elif login_status == 'logged':
            self.print_msg(self.full_phone, '帐号已登录')
            return True

    def save_session(self):
        '''
        将session字符串保存到txt
        '''
        pass

    def delete_session_file(self):
        '''
            删除已存在的对应号码的session文件, 避免重新登录的时候报错
        '''
        try:
            session_file = 'session/%s.session' % (self.full_phone)
            if os.path.exists(session_file):
                os.remove(session_file)
        except:
            pass

    def offline_user(self):
        if self.user_id:
            sql = "update user set status=-1 where id=%s" % (self.user_id)
            mysql.SqliteUI(sql, self.dbfile)


def TgGetSessionFunc(config_dict, que, rlock):
    ts = GetSessionClass(config_dict, que, rlock)
    ts.run()


class GetSessionClass(object):
    def __init__(self, config_dict, que, rlock):
        super(GetSessionClass, self).__init__()
        self.config_dict = config_dict
        self.dbfile = self.config_dict['dbfile']
        self.sql_class = mysql.MySqlite(self.dbfile)
        self.que = que
        self.rlock = rlock
        self.ld_path = self.config_dict['ld_path']
        self.live_dbfile = 'db/live.db'
        self.stop_thread = False

        self.ld = None
        self.index = None
        self.ld_ip = None

    def run(self):
        pass
        '''
        启动指定数量的模拟器
        判断模拟器是否安装了telegram, uiautomator2, clipboard等必装app, 没有则进行安装

        '''
        try:
            # 获取模拟器
            sql = "select * from account where status=1 limit 1"
            with self.rlock:
                sql_data = mysql.MySqlite(self.live_dbfile).select(sql)
                if sql_data:
                    self.ld_title = sql_data[0]['task']
                    self.index = sql_data[0]['type']
                    self.ld_ip = sql_data[0]['proxy']
                    mysql.MySqlite(self.live_dbfile).ui(
                        "update account set status=2 where type={}".format(
                            self.index))

            # 开始执行
            if self.index and self.ld_ip:
                # 模拟器实例
                self.ld = LD(self.ld_path, self.index)
                # 初始化模拟器,包括:安装并启动atx服务和相关app
                self.print_msg(self.ld_title, '初始化')
                self.initLd()

                # 主任务函数
                while True:
                    if self.stop_thread:
                        return True

                    # for _ in range(1):
                    # 判断注册任务是否完成
                    sql = "select count(id) as count from account where status=1 and length(session)>0"
                    sql_data = self.sql_class.select(sql)
                    if sql_data:
                        reg_num = sql_data[0]['count']
                        self.print_msg('已注册{}'.format(reg_num))
                        if reg_num >= self.config_dict['reg_count']:
                            self.print_msg(self.ld_title, '注册任务已完成')
                            return True

                    try:
                        self.main()
                    except Exception as e:
                        func.err_log("TelegramRegClass-main:{}".format(str(e)))
        except Exception as e:
            func.err_log('telegramReg:{}'.format(str(e)))
        finally:
            if self.index:
                with self.rlock:
                    mysql.MySqlite(self.live_dbfile).ui(
                        "update account set status=1 where type={}".format(
                            self.index))
            pass

    def main(self):
        # print(self.config_dict)
        '''
        获取模拟器
        初始化模拟器(安装atx, telegram等)
        恢复备份文件, 获取号码等信息
        teleton 注册
        模拟器获取验证码
        telethon输入验证码
        获取session
        '''
        self.tdict = {}  # 临时table, 用于存放各个步骤获取的数据
        self.tgfile, self.sql_id, self.session = None, None, None
        self.gz_path = None
        self.proxy_str = ""
        self.api_id, self.api_hash, self.first_name, self.last_name = None, None, None, None
        self.user_id, self.account_id = None, None
        self.pid, self.hwnd = None, None
        self.vcode = None
        self.task_status = False
        try:
            # 获取号码
            self.print_msg('开始获取号码')
            self.country, self.phone = self.get_phone()
            if self.country and self.phone:
                self.full_phone = '+' + self.country + self.phone
                self.print_msg(self.ld_title, '号码:', self.full_phone)
                # telegram操作实例
                self.tg = app.Telegram(self.ld_ip, self.ld)
                self.ld.killApp(self.tg.packagename)
                # 启动tai恢复数据
                self.tai = app.Tai(self.ld_ip, self.ld)
                self.ld.killApp(self.tai.packagename)

                self.tai.d.app_clear(self.tg.packagename)
                # 清空tai目录下所有文件
                _d = os.path.join(self.tai.app_dir, '*').replace('\\', '/')
                self.ld.ldConsole('rm -rf {}'.format(_d))

                # 复制备份文件到tai目录下
                pc_share = self.config_dict['pc_share'].replace('/', '\\')
                _d = self.gz_path.replace(pc_share,
                                          self.config_dict['ld_share'])
                _d = os.path.join(_d, '*').replace('\\', '/')
                con = 'cp  {} {}'.format(_d, self.tai.app_dir)  # 复制备份文件
                self.ld.ldConsole(con)
                # 恢复数据
                self.tai.startTai()  # 启动钛备份
                self.tai.restorApp('Telegram')  # 恢复tg数据

                # info_txt=os.path.join(self.gz_path,'info.txt')
                # self.yybl=app.YYBL(self.ld_ip,self.ld)
                # self.yybl.startAppByTxt('Telegram',info_txt)

                self.ld.runApp(self.tg.packagename)  # 启动tg
                self.tg.startApp()  # 确认tg是否启动
                if self.tg.tgIsOnline():  # 帐号在线,恢复成功
                    time.sleep(1)
                    if not self.tg.checkProxy() and self.config_dict['proxy']:
                        # 获取ip
                        set_proxy = False
                        for _ in range(5):
                            self.proxy_str = self.get_proxy()
                            self.print_msg(self.ld_title, '代理ip:',
                                           self.proxy_str)

                            if self.proxy_str:
                                mc = re.search(r'//(.*):(.*)', self.proxy_str)
                                if mc:
                                    proxy_ip = mc.group(1)
                                    port = mc.group(2)
                                    # print(proxy_ip,port)
                                    # 设置telegram代理ip
                                    if self.tg.setProxy(proxy_ip, port):
                                        set_proxy = True
                                        self.print_msg(self.ld_title, '代理设置成功')
                                        break
                        if not set_proxy:
                            self.print_msg(self.ld_title, '设置代理失败')
                            return

                    # 获取注册时需要的api_id和api_hash
                    api_id, api_hash = self.get_api_in_sql()
                    # insert task数据
                    if api_id and api_hash and self.phone:
                        log_dict = {}
                        log_dict['task'] = 'get_session'
                        log_dict['phone'] = "+" + self.country + self.phone
                        log_dict['target'] = '%s%s' % (self.country,
                                                       self.phone)
                        log_dict['account_id'] = self.account_id
                        log_dict['api_id'] = api_id
                        log_dict['api_hash'] = api_hash
                        log_dict['first_name'] = self.first_name
                        log_dict['last_name'] = self.last_name
                        log_dict['proxy_str'] = self.proxy_str
                        log_dict['dbfile'] = self.config_dict['dbfile']
                        mc = re.search(r'\d+', self.phone)
                        if mc:
                            se_key = mc.group()
                        session = 'session/%s' % (se_key)
                        # session文件
                        sfile = '%s.session' % session
                        if sfile:
                            with self.rlock:
                                self.sql_class.ui(
                                    "update account set path='{}' where id={} "
                                    .format(sfile, self.account_id))
                        log_dict['sfile'] = sfile
                        get_session_status = False
                        for _ in range(3):
                            self.print_msg(self.ld_title, self.full_phone,
                                           '开始获取session')
                            rdict = self.get_session(log_dict)
                            if rdict['status']:
                                get_session_status = True
                                break
                        if get_session_status:
                            self.session = rdict['resp']
                            # session结果写入到account表, 以备后续进行导出
                            if self.session:
                                self.print_msg(self.ld_title, self.full_phone,
                                               '获取session成功')
                                with self.rlock:
                                    self.sql_class.ui(
                                        "update account set status=1,session='%s',content='%s' where id=%s"
                                        % (self.session, self.proxy_str,
                                           self.account_id))

                                self.print_msg(self.ld_title, self.full_phone,
                                               'session:', self.session)
                                try:
                                    self.print_msg(self.ld_title,
                                                   self.full_phone, '获取api信息')
                                    self.get_api()
                                    # 设置密码
                                    if self.config_dict['set_password']:
                                        self.set_password()

                                    # 解决non-contact限制
                                    if self.config_dict['spambot']:
                                        self.print_msg(self.ld_title,
                                                       self.full_phone,
                                                       '开始解non-contact限制')
                                        # self.telet.spam_bot()
                                        if self.spam_bot():
                                            self.print_msg(
                                                self.ld_title, self.full_phone,
                                                '解non-contact限制-完成')

                                    # 移动备份文件到session目录下
                                    to_dir = os.path.join(
                                        self.config_dict['pc_share'],
                                        'Session')
                                    shutil.move(self.gz_path, to_dir)
                                except Exception as e:
                                    self.print_msg(self.ld_title,
                                                   self.full_phone, str(e))
                                    # func.err_log(str(e))
                                finally:
                                    return True
                        else:
                            mysql.SqliteUI(
                                "update account set status=-1 where id=%s" %
                                (self.account_id), self.dbfile)
                            if rdict['resp']:
                                self.print_msg(
                                    self.ld_title,
                                    '获取session失败: %s' % rdict['resp'])
                            else:
                                self.print_msg(self.ld_title, '获取session失败')
                else:
                    self.print_msg(self.ld_title, self.full_phone, '已掉线')
                    self.sql_class.ui(
                        "update account set status=-1 where id={}".format(
                            self.account_id))
                    to_dir = os.path.join(self.config_dict['pc_share'],
                                          'Offline')
                    shutil.move(self.gz_path, to_dir)

        finally:
            # # 释放号码
            # self.release_phone()
            pass
            # # 关闭客户端
            # if self.pid and self.hwnd:
            #     self.print_msg(self.full_phone,'关闭客户端')
            #     self.tg.close_client(self.tgfile)

    # 初始化模拟器,
    def initLd(self):
        '''初始化模拟器,包括:安装并启动atx服务和相关app'''
        self.ld.installApps()
        self.ld.runAtx()
        pass

    # 随机获取头像图片文件
    def get_avatar_img(self, folder):
        '''随机获取头像图片文件'''
        img_list = []
        if os.path.exists(folder) and os.path.isdir(folder):
            flist = os.listdir(folder)
            for f in flist:
                if '.jpg' in f or '.png' in flist:
                    img_list.append(f)
            if img_list:
                img = random.choice(img_list)
                if img:
                    img = os.path.join(folder, img)
                    _tmp_img = func.copy_tmp_img(img)
                    if _tmp_img:
                        return _tmp_img

    # 从目录随机复制图片到模拟器中(并广播), 用于图片上传
    def copyAvatar(self):
        source_dir = self.config_dict['avatar']
        pc_share = self.config_dict['pc_share']
        ld_share = self.config_dict['ld_share']
        tmp_img = self.get_avatar_img(source_dir)  # 获取随机图片
        img_name = os.path.basename(tmp_img)
        if tmp_img:
            pass
            # 将随机图片复制到模拟器电脑共享目录下
            pc_share_img = os.path.join(pc_share, img_name).replace('\\', '/')
            print('pc_share_img', pc_share_img)
            shutil.move(tmp_img, pc_share_img)
            if os.path.exists(pc_share_img):
                # 广播刷新图库
                resp = self.ld.ldConsole(
                    'am broadcast -a android.intent.action.MEDIA_MOUNTED -d file://{}'
                    .format(ld_share))
                print(resp)
                ld_share_img = os.path.join(ld_share, img_name)
                print(ld_share_img)
                return ld_share_img

    def print_msg(self, *args):
        '''
        打印日志到UI界面
        '''
        m = " "
        if args:
            m = m.join([str(x) for x in args])
        # self.mdict['msg']=m
        try:
            self.que.put(m)
        except:
            pass

    def get_phone(self):
        '''获取号码  []返回[country:国码; phone: 电话号码; tid: api记录id,用于释放]'''
        country = None
        phone = None
        if self.config_dict['platform'] == 'LocalGZ':

            sql = "select * from account where status!=1 and type='LocalGZ'  and task='reg_class' order by use_num asc limit 1"
            with self.rlock:
                sql_data = self.sql_class.select(sql)
                if sql_data:
                    self.account_id = sql_data[0]['id']
                    phone = sql_data[0]['phone']
                    mc = re.search(r'\d+', self.config_dict['country'])
                    if mc:
                        country = mc.group(0)
                        if '+' in phone:
                            phone = phone.replace('+', '')
                        phone = phone[len(country):len(phone)]
                    self.gz_path = sql_data[0]['data']
                    self.sql_class.ui(
                        "update account set use_num=use_num+1 where id={}".
                        format(self.account_id))
                if phone and country:
                    return country, phone

        return None, None

    def get_api_in_sql(self):
        # 从数据库中获取, 如果没有则随机有效信息
        # sql="select * from account where api_id is not null and api_hash is not null and length(api_id)>5 and length(api_hash)>10 order by random() limit 1"
        # tmp_data=mysql.SqliteSelect(sql,self.dbfile)
        # if tmp_data and len(tmp_data)>0 and len(tmp_data[0]['api_id'])>5 and len(tmp_data[0]['api_hash'])>10:
        #     api_id=tmp_data[0]['api_id']
        #     api_hash=tmp_data[0]['api_hash']
        # else:
        #     api_list=[['1822649','6be76876b84a8149ece1c418524a3cc6'],['1978922','988734fe7f8a912b94f046b48c6dd932'],['1861739','2be21bcc603cde584ee8896e5272914e'],['1951154','5ae880d8b7d6f9b83a1113dd09db1106'],['1504261','f3b966835bc67cbfd8155e275fd49b07'],['2347264','26c48259bd538fd53fe41bc91155fb6c'],['2516785','2b098f1e75c471d39fbe3dc923789bc6'],['2869586','4188b2a4515b3c86b080392c53e7f40f'],['2006874','44db0882f8d1ffd433b86d31fd7065fd'],['2159791','5d89b723204e8c8fcaf36cf1278599d0'],['2899996','811c8e6e1c4667d8030898214146ccc6'],['2370942','928c08af9f4f0803679de643b6c668d7'],['2561072','982c1c5f8a17eb531107d368a7f95ec1'],['2179088','9889e2eec5f24056f8dd4d0c4ad050b1'],['2432202','9e2ec24bf651b7041880302f6190dd86'],['2477971','b4db23aff65c3a9d0d70a08ea7c29922'],['2559656','d08b2470b6f72cc44c6266ebcb41a0d7'],['2734493','dd985add75e91fe4389ae36f792454b2'],['2079217','e1ed7b324ee08641993c08a1d039f6e2'],['2385812','e219d8985bee383421bf83e97116052a'],['2664742','f7bd02dd2af17eac6b6dd0e1d62e6895']]
        #     api_info=random.choice(api_list)
        #     api_id=api_info[0]
        #     api_hash=api_info[1]
        sql = "select * from api where status=1 order by random() limit 1"
        sql_data = mysql.MySqlite(self.dbfile).select(sql)
        if sql_data:
            api_id = sql_data[0]['api_id']
            api_hash = sql_data[0]['api_hash']
        return api_id, api_hash

    def get_proxy(self):
        '''获取代理ip'''
        sql = "select * from proxy where status=1 order by random() limit 1"
        sql_data = mysql.SqliteSelect(sql, 'db/proxy.db')
        if sql_data:
            proxy_str = sql_data[0]['proxy_str']
            return proxy_str
        else:
            return ""

    def spam_bot(self):
        log_dict = {}
        log_dict['task'] = 'spam_bot'
        log_dict['target'] = 'me'
        log_dict['phone'] = "+" + self.country + self.phone
        log_dict['session'] = self.session
        log_dict['proxy_str'] = self.proxy_str
        log_dict['from_id'] = '777000'
        log_dict['dbfile'] = self.config_dict['dbfile']
        tgf = telethon_func.TelethonFunc(log_dict)
        result_dict = tgf.run()
        if result_dict['status']:
            return True

    # 设置密码
    def set_password(self):
        self.print_msg(self.full_phone, '开始设置密码')
        log_dict = {}
        log_dict['task'] = 'set_password'
        log_dict['phone'] = "+" + self.country + self.phone
        log_dict['target'] = 'me'
        log_dict['proxy_str'] = self.proxy_str
        log_dict['session'] = self.session
        log_dict['dbfile'] = self.config_dict['dbfile']
        log_dict['account_id'] = self.account_id
        log_dict['password'] = "{}_{}".format('wuya88.com', func.RandomStr(7))
        # print(log_dict)
        tgf = telethon_func.TelethonFunc(log_dict)
        result_dict = tgf.run()
        if result_dict['status']:  # 修改成功
            # 更新密码到表
            with self.rlock:
                _sql = "update account set password='{}' where id={} ".format(
                    log_dict['password'], self.account_id)
                self.sql_class.ui(_sql)
        self.print_msg(log_dict['phone'], result_dict['resp'])
        # print(result_dict)
        # print('================================================')

    def get_nickname(self):
        '''获取昵称[]返回:[first_name; last_name]'''
        if self.config_dict['random_nickame']:  # 随机昵称
            first_name = func.GBK2312(random.randint(1, 2))
            last_name = func.GBK2312(random.randint(2, 3))
            return first_name, last_name
        else:  # 列表中取昵称
            sql = "select * from content where type='nickname' order by random() limit 1"
            # sql_data=mysql.SqliteSelect(sql,self.dbfile)
            sql_data = self.sql_class.select(sql)
            if sql_data:
                nickname_str = sql_data[0]['content']
                if nickname_str:
                    mc = re.search(r'(.*?)\|(.*)', nickname_str)
                    if mc:
                        first_name = mc.group(1)
                        last_name = mc.group(2)
                    else:
                        first_name = nickname_str[0:int(len(nickname_str) / 2)]
                        last_name = nickname_str[int(len(nickname_str) /
                                                     2):len(nickname_str)]
                    return first_name, last_name

    #     return sql_id
    def get_session(self, log_dict):
        '''获取session字符[sql_id:数据库id]返回[true/fasle ,session 字符串存储到数据库和txt中]'''
        tgf = telethon_func.TelethonFunc(log_dict, None, self.getCodeInLd)
        result_dict = tgf.get_session()
        return result_dict

    def getCodeInLd(self):
        '''从模拟器app中获取验证码'''
        self.tg.searchKeyword('Telegram')
        code = self.tg.getLoginCode()
        self.print_msg(self.ld_title, self.full_phone, '验证码:{}'.format(code))
        return code

    def get_api(self):
        '''获取api信息'''
        try:
            for _ in range(3):
                random_hash = api.MyTelegramOrg_SendPassword(
                    self.country, self.phone, self.proxy_str)
                if random_hash:
                    break
            # print(random_hash)
            if random_hash:
                log_dict = {}
                log_dict['task'] = 'get_msg'
                log_dict['target'] = 'me'
                log_dict['phone'] = "+" + self.country + self.phone
                log_dict['session'] = self.session
                log_dict['proxy_str'] = self.proxy_str
                log_dict['from_id'] = '777000'
                log_dict['dbfile'] = self.config_dict['dbfile']
                tgf = telethon_func.TelethonFunc(log_dict)
                result_dict = tgf.run()
                if result_dict['status']:
                    msg = result_dict['resp']
                    # print(msg)
                    # 匹配验证码
                    if msg and 'my.telegram.org' in msg:
                        mc = re.search(
                            r'my.telegram.org.*?[,|:]([\s\S]*?)\s\s',
                            msg)  # 匹配
                        if not mc:
                            mc = re.search(r'([a-zA-Z0-9]*?\-.*)', msg)  #
                        if mc:
                            web_login_code = mc.group(1)
                            # 获取登陆后的cookie字典
                            if web_login_code:
                                # print('web_login_code',web_login_code)
                                cookie_dict = api.MyTelegramOrg_Login(
                                    self.country, self.phone, random_hash,
                                    web_login_code, self.proxy_str)
                                if cookie_dict:
                                    cookie = "stel_token=" + cookie_dict[
                                        'stel_token']
                                    res_dict = api.MyTelegramOrg_App(
                                        self.phone, cookie,
                                        self.proxy_str)  # 获取api_id api_hash
                                    # print(res_dict)
                                    if res_dict:
                                        # print(res_dict)
                                        sql = "update account set api_id='%s',api_hash='%s' where id=%s" % (
                                            res_dict['api_id'],
                                            res_dict['api_hash'],
                                            self.account_id)
                                        # mysql.SqliteUI(sql,self.dbfile)
                                        self.sql_class.ui(sql)
                                        mysql.MySqlite(self.dbfile).insert(
                                            "insert into api (status,api_id,api_hash) values (1,'{}','{}')"
                                            .format(res_dict['api_id'],
                                                    res_dict['api_hash']))
                                        self.print_msg(self.full_phone,
                                                       'api信息设置成功')
                                        return True
        except Exception as e:
            func.err_log("get_api:" + str(e))

    def get_telethon_code(self):
        '''
        通过telethon获取登陆验证码
        '''
        log_dict = {}
        log_dict['task'] = 'get_msg'
        log_dict['target'] = 'me'
        log_dict['phone'] = "+" + self.country + self.phone
        log_dict['session'] = self.session
        log_dict['proxy_str'] = self.proxy_str
        log_dict['from_id'] = '777000'
        log_dict['dbfile'] = self.config_dict['dbfile']
        tgf = telethon_func.TelethonFunc(log_dict)
        result_dict = tgf.run()
        if result_dict['status']:
            msg = result_dict['resp']
            if msg and 'Login code' in msg:
                mc = re.search(r'\d{5,}', msg)
                if mc:
                    vcode = mc.group(0)
                    return vcode

    def save_session(self):
        '''
        将session字符串保存到txt
        '''
        pass

    def delete_session_file(self):
        '''
            删除已存在的对应号码的session文件, 避免重新登录的时候报错
        '''
        try:
            session_file = 'session/%s.session' % (self.full_phone)
            if os.path.exists(session_file):
                os.remove(session_file)
        except:
            pass

    def offline_user(self):
        if self.user_id:
            sql = "update user set status=-1 where id=%s" % (self.user_id)
            mysql.SqliteUI(sql, self.dbfile)


def initAllDB(dbfile):
    sql = mysql.MySqlite(dbfile)
    sql.init_db()
