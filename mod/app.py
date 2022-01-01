# -*- coding:utf-8 -*-
import time, os, sys, re, random, string
import mod.func as func
import uiautomator2 as u2


class Telegram(object):
    def __init__(self, ip, ld):
        self.ip = ip
        self.ld = ld
        self.packagename = 'org.telegram.messenger'
        self.d = u2.connect(self.ip)
        self.page = self.uiDict()

    def run(self):
        print(self.d.info)
        pass

    def uiDict(self):
        page = {}
        page['首页'] = {}
        page['首页']['connecting'] = self.d.xpath(
            '//android.widget.TextView[contains(@text,"Connect")]')
        page['首页']['StartMessaging'] = self.d.xpath(
            '//*[@text="Start Messaging"]')
        page['首页']['YourPhone'] = self.d.xpath('//*[@text="Your Phone"]')
        page['首页']['提交号码'] = self.d.xpath('//*[@content-desc="Done"]')
        page['代理'] = {}
        page['代理']['UseProxy'] = self.d.xpath('//*[@text="Use Proxy"]')
        page['代理']['AddProxy'] = self.d.xpath('//*[@text="Add Proxy"]')
        page['代理']['EditProxy'] = self.d.xpath('//*[@content-desc="Edit"]')
        page['代理']['Socks5Proxy'] = self.d.xpath('//*[@text="SOCKS5 Proxy"]')
        page['代理']['IP'] = self.d.xpath(
            '//android.widget.ScrollView/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.EditText[1]'
        )
        page['代理']['端口'] = self.d.xpath(
            '//android.widget.ScrollView/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[2]/android.widget.EditText[1]'
        )
        page['代理']['代理有效'] = self.d.xpath('//*[contains(@text,"Available")]')
        page['代理']['已连接'] = self.d.xpath('//*[contains(@text,"Connected")]')
        page['注册'] = {}
        page['注册']['国码'] = self.d.xpath(
            '//android.widget.ScrollView/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.EditText[1]'
        )
        page['注册']['号码'] = self.d.xpath(
            '//android.widget.ScrollView/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.EditText[2]'
        )
        page['注册']['CheckYourMessage'] = self.d.xpath(
            '//android.widget.TextView[@text="Check your Telegram messages"]')
        page['注册']['SendSMS'] = self.d.xpath(
            '//android.widget.TextView[@text="Send the code as an SMS"]')
        page['注册']['GoBack'] = self.d.xpath('//*[@content-desc="Go back"]')
        page['注册']['EnterCode'] = self.d.xpath('//*[@text="Enter code"]')
        page['注册']['已发送验证码提示'] = self.d.xpath(
            '//*[contains(@text,"We’ve sent an SMS with an activation code to your phone")]'
        )
        page['注册']['Code1'] = self.d.xpath(
            '//android.widget.ScrollView/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.EditText[1]'
        )
        page['注册']['Code2'] = self.d.xpath(
            '//android.widget.ScrollView/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.EditText[2]'
        )
        page['注册']['Code3'] = self.d.xpath(
            '//android.widget.ScrollView/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.EditText[3]'
        )
        page['注册']['Code4'] = self.d.xpath(
            '//android.widget.ScrollView/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.EditText[4]'
        )
        page['注册']['Code5'] = self.d.xpath(
            '//android.widget.ScrollView/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.EditText[5]'
        )
        page['注册']['TooManyAttemps'] = self.d.xpath(
            '//*[@text="Too many attempts, please try again later."]')
        page['注册']['PhoneBanned'] = self.d.xpath(
            '//android.widget.TextView[@text="This phone number is banned."]')
        page['注册']['InvalidCode'] = self.d.xpath(
            '//*[contains(@text,"Invalid code")]')
        page['注册']['YourName'] = self.d.xpath('//*[@text="Your Name"]')
        page['注册']['FirstName'] = self.d.xpath(
            '//*[contains(@text,"First name")]')
        page['注册']['LastName'] = self.d.xpath(
            '//*[contains(@text,"Last name")]')
        page['注册']['Done'] = self.d.xpath('//*[@content-desc="Done"]')
        page['已登录'] = {}
        page['已登录']['选项'] = self.d.xpath(
            '//*[@content-desc="Open navigation menu"]')
        page['已登录']['Settings'] = self.d.xpath('//*[@text="Settings"]')
        page['已登录']['个人信息页-Account'] = self.d.xpath(
            '//android.widget.TextView[@text="Account"]')
        page['已登录']['NoUsername'] = self.d.xpath('//*[@text="Username: None"]')
        page['已登录']['Username'] = self.d.xpath('//*[@text="Username"]')
        page['已登录']['User_name'] = self.d.xpath(
            '//*[@text="Username"]/parent::*/android.widget.TextView[1]')
        page['已登录']['Username输入框'] = self.d.xpath('//android.widget.EditText')
        page['已登录']['已有username'] = self.d.xpath(
            '//android.widget.TextView[contains(@text,"https://t.me/")]')
        page['已登录']['Username提交按钮'] = self.d.xpath(
            '//android.widget.ImageButton[@content-desc="Done"]')
        page['已登录']['Username已存在'] = self.d.xpath(
            '//*[@text="Sorry, this username is already taken."]')
        page['已登录']['Username可用'] = self.d.xpath(
            '//*[contains(@text,"is available.")]')
        page['已登录']['安全设置'] = self.d.xpath(
            '//android.widget.TextView[@text="Privacy and Security"]')
        page['已登录']['两步设置'] = self.d.xpath(
            '//*[@text="Two-Step Verification"]')
        page['已登录']['设置密码按钮'] = self.d.xpath('//*[@text="Set Password"]')
        page['已登录']['密码输入框'] = self.d.xpath(
            '//android.widget.ScrollView/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]'
        )
        page['已登录']['密码提交按钮'] = self.d.xpath('//*[@text="Continue"]')
        page['已登录']['二次密码输入框'] = self.d.xpath(
            '//android.widget.ScrollView/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]'
        )
        page['已登录']['Hit输入框'] = self.d.xpath(
            '//android.widget.ScrollView/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]'
        )
        page['已登录']['RecoveryEmail'] = self.d.xpath(
            '//*[@text="Recovery Email"]')
        page['已登录']['Skip按钮'] = self.d.xpath('//*[@text="Skip"]')
        page['已登录']['Skip按钮-浮窗'] = self.d.xpath('//*[@text="SKIP"]')
        page['已登录']['密码设置成功'] = self.d.xpath('//*[@text="Return to Settings"]')
        page['已登录']['头像图片'] = self.d.xpath('//*[@text="Profile picture"]')
        page['已登录']['头像正在上传中标识'] = self.d.xpath(
            '//*[@text="Profile picture"]/parent::*/android.view.View[2]')
        page['已登录']['SetProfilePhoto'] = self.d.xpath(
            '//*[@text="Set Profile Photo"]')
        page['已登录']['照片选择浮窗'] = self.d.xpath(
            '//*[@text="Choose photo or video"]')
        page['已登录']['照片框'] = self.d.xpath(
            '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.View[1]/android.widget.FrameLayout'
        )
        page['已登录']['照片Send按钮'] = self.d.xpath('//*[@content-desc="Send"]')
        page['已登录']['更换照片按钮'] = self.d.xpath(
            '//*[@content-desc="Change profile picture"]')
        page['已登录']['搜索按钮'] = self.d.xpath('//*[@content-desc="Search"]')
        page['已登录']['新消息'] = self.d.xpath('//*[@content-desc="New Message"]')
        page['已登录']['搜索输入框'] = self.d.xpath('//*[@text="Search"]')

        page['已登录']['telegram官方'] = self.d.xpath(
            '//android.view.View[contains(@text,"Telegram") and contains(@text,"support")]'
        )
        page['已登录']['LoginCode'] = self.d.xpath(
            '//android.view.View[contains(@content-desc,"Login code")]')
        page['已登录']['返回按钮'] = self.d.xpath(
            '//android.widget.ImageView[@content-desc="Go back"]')
        page['已登录']['NewGroup'] = self.d.xpath('//*[@text="New Group"]')
        page['已登录']['AddPeople'] = self.d.xpath('//android.widget.EditText')
        page['已登录']['NextButton'] = self.d.xpath('//*[@content-desc="Next"]')
        page['已登录']['EnterGroupName'] = self.d.xpath(
            '//*[@text="Enter group name"]')
        page['已登录']['DoneButton'] = self.d.xpath('//*[@content-desc="Done"]')
        page['已登录']['GroupInputBox'] = self.d.xpath(
            '//android.widget.EditText')

        return page

    def startTg(self):
        self.d.app_clear(self.packagename)
        time.sleep(3)
        # self.d.app_start(self.packagename)
        self.ld.runApp(self.packagename)
        time.sleep(3)
        self.page['首页']['StartMessaging'].click_exists(5)

    def startApp(self):
        self.page['首页']['StartMessaging'].click_exists(5)

    def tgIsOnline(self):
        for _ in range(10):
            if self.page['首页']['StartMessaging'].exists:  # 已掉线
                return
            if self.page['已登录']['搜索按钮'].exists:
                return True
            time.sleep(1)

    def checkProxy(self):
        if self.page['首页']['connecting'].exists:
            return
        else:
            return True

    def setProxy(self, ip, port):
        if self.page['首页']['connecting'].wait(3):
            self.page['首页']['connecting'].click_exists(3)
            time.sleep(1)
            if self.page['代理']['EditProxy'].exists:
                self.page['代理']['EditProxy'].click()
            elif self.page['代理']['AddProxy'].exists:
                self.page['代理']['AddProxy'].click()
            time.sleep(1)
            # self.page['代理']['UseProxy'].click_exists(3)
            # time.sleep(1)
            self.adbInputText(self.page['代理']['IP'], ip, True, 17)  # 输入ip
            self.page['代理']['端口'].set_text(port)  # 输入端口
            # self.adbInputText(self.page['代理']['端口'],port)
            self.d.click(0.932, 0.091)  # 点击提交按钮
            for _ in range(20):
                if self.page['代理']['代理有效'].exists:
                    self.d.click(0.882, 0.161)  # 点击use proxy
                    time.sleep(2)
                    self.backToEl(
                        [self.page['首页']['提交号码'], self.page['已登录']['搜索按钮']])
                    return True
                elif self.page['代理']['已连接'].exists:
                    time.sleep(2)
                    self.backToEl(
                        [self.page['首页']['提交号码'], self.page['已登录']['搜索按钮']])
                    return True
                else:
                    time.sleep(1)
            self.backToEl([self.page['首页']['提交号码'], self.page['已登录']['搜索按钮']])
        elif self.page['首页']['YourPhone'].wait(2):
            return True

    def inputPhone(self, country, phone):
        '''输入电话号码[country:国码; phone:电话]'''
        time.sleep(1)
        # self.page['注册']['国码'].set_text(country)
        # self.page['注册']['号码'].set_text(phone)
        self.page['注册']['号码'].click()
        for _ in range(15):
            self.d.press('delete')

        self.adbInputText(self.page['注册']['国码'], country)
        self.adbInputText(self.page['注册']['号码'], phone)

        self.page['首页']['提交号码'].click()
        for _ in range(20):
            if self.page['注册']['PhoneBanned'].exists:
                self.d.press('back')
                return
            if self.page['注册']['TooManyAttemps'].exists:
                return
            if self.page['注册']['SendSMS'].exists:
                # print('获取到SendSMS')
                self.page['注册']['SendSMS'].click()
            if self.page['注册']['EnterCode'].exists:
                return True

            time.sleep(1)

    def inputCode(self, code):
        '''输入验证码[code:验证码]'''
        if code and self.page['注册']['EnterCode'].exists:
            li = func.splitStrByLen(code, 1)  # 分割验证码

            c = [
                self.page['注册']['Code1'], self.page['注册']['Code2'],
                self.page['注册']['Code3'], self.page['注册']['Code4'],
                self.page['注册']['Code5']
            ]
            # self.d.set_fastinput_ime(True) # 切换成FastInputIME输入法
            for i in range(len(li)):
                c[i].click()
                # self.d.send_keys(li[i]) # adb广播输入
                self.ld.adbInputText(li[i])
            # self.d.set_fastinput_ime(False) # 切换成正常的输入法
            if self.page['注册']['Code1'].wait_gone(15):
                return True
            else:
                return

    # 输入昵称
    def inputNickname(self, first_name, last_name):
        if self.page['注册']['YourName'].wait(3):
            self.page['注册']['FirstName'].set_text(first_name)
            self.page['注册']['LastName'].set_text(last_name)
            self.page['注册']['Done'].click()
            time.sleep(1)
            return True

    def searchKeyword(self, kw):
        for _ in range(10):
            if self.page['已登录']['搜索按钮'].exists:
                self.page['已登录']['搜索按钮'].click()
                if self.page['已登录']['搜索输入框'].wait(3):
                    break
                time.sleep(1)

        if self.page['已登录']['搜索输入框'].exists:
            self.page['已登录']['搜索输入框'].set_text(kw)
            if self.page['已登录']['telegram官方'].wait(10):
                self.page['已登录']['telegram官方'].click()
                return True

    def getLoginCode(self):
        '''获取验证码'''
        code = None
        if self.page['已登录']['返回按钮'].wait(5):
            msg = None
            # 获取所有view, 筛选最后内容
            for el in self.d.xpath('//android.view.View').all():
                info = el.info
                if info['contentDescription'] and 'code' in info[
                        'contentDescription']:
                    msg = info['contentDescription']
            if msg:
                mc = re.search(r'\d{5,}', msg)
                if mc:
                    code = mc.group()
        self.backToEl(self.page['已登录']['搜索按钮'])
        return code

    def setUsername(self):
        # print('开始设置username')
        username = None
        self.page['已登录']['选项'].click()
        self.page['已登录']['Settings'].click()
        self.page['已登录']['Username'].wait()
        uname = self.page['已登录']['User_name'].info['text']
        if uname == 'None':  # 无用户名
            self.page['已登录']['Username'].click()
            username_ok = False
            for _ in range(5):
                if self.page['已登录']['Username输入框'].wait(3):
                    username = self.page['已登录']['Username输入框'].info['text']
                    if ' ' in username:
                        username = None
                if username:
                    self.backToIndex()
                    return username
                username = func.RandomUsername()
                self.adbInputText(self.page['已登录']['Username输入框'], username,
                                  True, 10)
                for _ in range(20):
                    if self.page['已登录']['Username可用'].exists:
                        username_ok = True
                        break
                if username_ok:
                    break
            if username_ok:
                for _ in range(3):
                    self.page['已登录']['Username提交按钮'].click()
                    for _ in range(10):
                        time.sleep(1)
                        uname = self.page['已登录']['User_name'].info['text']
                        if not uname == 'None':
                            username = uname.replace('@', '')
                            self.backToIndex()
                            return username
        else:
            username = uname.replace('@', '')
            # 已经有username了
            pass
        self.backToIndex()
        return username

    def setPassword(self, password=None):
        print('开始设置密码')
        self.backToIndex()
        password = "{}_{}".format('wuya88.com', func.RandomStr(7))
        self.page['已登录']['选项'].click()
        self.page['已登录']['Settings'].click()
        self.page['已登录']['安全设置'].click()
        self.page['已登录']['两步设置'].click()
        time.sleep(2)
        self.page['已登录']['设置密码按钮'].click()
        self.adbInputText(self.page['已登录']['密码输入框'], password)
        self.page['已登录']['密码提交按钮'].click()
        time.sleep(2)
        self.adbInputText(self.page['已登录']['二次密码输入框'], password)
        self.page['已登录']['密码提交按钮'].click()
        time.sleep(2)
        self.adbInputText(self.page['已登录']['Hit输入框'], 'www.wuya88.com')
        self.page['已登录']['密码提交按钮'].click()
        time.sleep(2)
        if self.page['已登录']['RecoveryEmail'].exists:
            self.page['已登录']['Skip按钮'].click()
            self.page['已登录']['Skip按钮-浮窗'].click()
            self.page['已登录']['密码设置成功'].click_exists(5)

        pass

    def createChannel(self, channel_name, invite_username='wuya88bot'):
        if '@' not in invite_username:
            invite_username = '@' + invite_username
        self.backToIndex()
        self.page['已登录']['选项'].click()
        self.page['已登录']['NewGroup'].click()
        self.page['已登录']['AddPeople'].set_text(invite_username)
        xp = self.d.xpath(
            '//android.widget.TextView[@text="{}"]'.format(invite_username))
        for _ in range(10):
            if xp.exists:
                xp.click()
                time.sleep(1)
                if self.page['已登录']['NextButton'].exists:
                    break
            time.sleep(1)
        if self.page['已登录']['NextButton'].wait(5):
            self.page['已登录']['NextButton'].click()
            if self.page['已登录']['EnterGroupName'].wait(5):
                self.page['已登录']['EnterGroupName'].set_text(channel_name)
                self.page['已登录']['DoneButton'].click()
                for _ in range(20):
                    if self.page['已登录']['GroupInputBox'].exists:
                        time.sleep(7)
                        self.backToIndex()
                        return True
                    time.sleep(1)

    def uploadAvatar(self, img):
        # print('开始上传头像')
        self.backToIndex()
        self.page['已登录']['选项'].click()
        self.page['已登录']['Settings'].click()
        img_l = os.path.split(img)
        if self.page['已登录']['SetProfilePhoto'].wait(2):
            for _ in range(3):
                co = 'am broadcast -a android.intent.action.MEDIA_MOUNTED -d file://{}'.format(
                    img_l[0])
                self.ld.ldConsole(co)
                time.sleep(10)
                self.page['已登录']['SetProfilePhoto'].click()
                time.sleep(1)
                if self.page['已登录']['照片选择浮窗'].wait(2):
                    time.sleep(.5)
                    els = self.page['已登录']['照片框'].all()  # 所有照片框元素
                    el_list = []  # 有照片的元素列表
                    for el in els:
                        if el.text == 'Photo':
                            el_list.append(el)
                    if el_list:
                        e = random.choice(el_list)  # 随机选一张照片
                        e.click()
                        time.sleep(1)
                        self.page['已登录']['照片Send按钮'].click()
                        time.sleep(3)
                        for _ in range(25):
                            if self.page['已登录']['头像图片'].exists:
                                if not self.page['已登录']['头像正在上传中标识'].exists:
                                    return True
                            else:
                                break
                            time.sleep(1)
                    else:
                        self.backToEl(self.page['已登录']['SetProfilePhoto'])
                        time.sleep(1)
        elif self.page['已登录']['头像图片'].wait(3):
            self.backToIndex()
            return True

        pass

    # 判断是否在首页
    def isIndexPage(self):
        if self.page['已登录']['搜索按钮'].wait(5):
            return True

    # 回退到指定元素
    def backToEl(self, el):
        '''回退到指定元素[el:元素][返回:Bool]'''
        for _ in range(10):
            if type(el) == list:
                for e in el:
                    if e.exists:
                        return True
            else:
                if el.exists:
                    return True
            self.d.press('back')
            time.sleep(1)

    # 回到首页
    def backToIndex(self):
        self.backToEl(self.page['已登录']['选项'])

    def testFunc(self):
        xp = '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.View[1]/android.widget.FrameLayout'
        xpd = self.d.xpath(xp)
        els = xpd.all()
        if els:
            for el in els:
                # print(el.info)
                sxp = self.d.xpath(xp + '/android.widget.FrameLayout[1]')
                print(sxp.info)

    # 使用adb输入内容
    def adbInputText(self, el, text, delete=False, del_num=5):
        el.click()
        if delete:
            for _ in range(del_num):
                self.d.press('delete')
        self.ld.adbInputText(text)


class Tai(object):
    def __init__(self, ip, ld):
        self.ip = ip
        self.ld = ld
        self.packagename = 'com.keramidas.TitaniumBackup'
        self.d = u2.connect(self.ip)
        self.page = self.uiDict()
        self.app_dir = '/storage/emulated/legacy/TitaniumBackup'

    def uiDict(self):
        page = {}
        page['首页'] = {}
        page['首页']['永远记住'] = self.d.xpath(
            '//*[@resource-id="com.android.settings:id/remember_forever"]')
        page['首页']['允许'] = self.d.xpath(
            '//*[@resource-id="com.android.settings:id/allow"]')
        page['首页']['首次运行'] = self.d.xpath(
            '//*[@resource-id="android:id/alertTitle" and contains(@text,"首次运行")]'
        )
        page['首页']['确认按钮'] = self.d.xpath(
            '//*[@resource-id="android:id/buttonPanel"]/android.widget.LinearLayout[1]'
        )
        page['首页']['不要再显示此内容'] = self.d.xpath(
            '//*[contains(@text,"不要再显示此内容")]')
        page['首页']['弹窗-确认'] = self.d.xpath('//*[@text="确定"]')
        page['首页']['基本信息'] = self.d.xpath('//*[@text="基本信息"]')
        page['首页']['备份/还原'] = self.d.xpath('//*[@text="备份/还原"]')
        page['首页']['点击编辑过滤器'] = self.d.xpath('//*[@text="点击编辑过滤器"]')
        page['首页']['app名称'] = self.d.xpath('//android.widget.EditText')
        page['首页']['应用'] = self.d.xpath('//*[@content-desc="应用"]')
        page['首页']['备份提示'] = self.d.xpath(
            '//*[contains(@text,"个备份") and contains(@text,"上一次")]')
        page['首页']['未备份'] = self.d.xpath('//*[@text="未备份"]')
        page['首页']['备份/还原'] = self.d.xpath('//*[@text="备份/还原"]')
        page['首页']['点击编辑过滤器'] = self.d.xpath('//*[@text="点击编辑过滤器"]')
        page['首页']['编辑框'] = self.d.xpath('//android.widget.EditText')
        page['首页']['应用按钮'] = self.d.xpath('//*[@content-desc="应用"]')
        page['首页']['abc'] = self.d.xpath(
            '//android.widget.ListView/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]'
        )
        page['首页']['Telegram备份列表'] = self.d.xpath(
            '//*[contains(@text,"Telegram")]')
        page['首页']['备份按钮'] = self.d.xpath(
            '//android.widget.Button[contains(@text,"备份")]')
        page['首页']['正在备份弹窗'] = self.d.xpath(
            '//*[@resource-id="android:id/alertTitle"]')
        page['首页']['恢复按钮'] = self.d.xpath(
            '//android.widget.Button[@text="恢复"]')
        page['首页']['恢复-数据按钮'] = self.d.xpath(
            '//*[@resource-id="android:id/button2"]')
        page['首页']['app正在运行提示'] = self.d.xpath(
            '//*[@resource-id="android:id/message" and contains(@text,"正在运行")]'
        )
        page['首页']['确定结束按钮'] = self.d.xpath(
            '//*[@resource-id="android:id/button1"]')
        page['首页']['正在恢复弹窗'] = self.d.xpath(
            '//*[@resource-id="android:id/alertTitle" and contains(@text,"正在恢复")]'
        )

        return page

    def startTai(self):
        self.ld.runApp(self.packagename)
        for _ in range(5):
            if self.page['首页']['永远记住'].exists:
                self.page['首页']['永远记住'].click()
                time.sleep(3)
                self.page['首页']['允许'].click()
                time.sleep(.5)
            if self.page['首页']['首次运行'].exists:
                self.d.press('back')
                time.sleep(.5)
            if self.page['首页']['不要再显示此内容'].exists:
                self.page['首页']['不要再显示此内容'].click()
                self.page['首页']['弹窗-确认'].click()
                time.sleep(.5)
            if self.page['首页']['基本信息'].exists:
                return True
            self.d.press('back')
            time.sleep(1)

    def backupApp(self, app_name):
        self.page['首页']['备份/还原'].click()
        time.sleep(.5)
        if self.page['首页']['Telegram备份列表'].exists:
            self.page['首页']['Telegram备份列表'].click()
        else:
            self.page['首页']['点击编辑过滤器'].click()
            self.adbInputText(self.page['首页']['编辑框'],
                              app_name,
                              delete=True,
                              del_num=10)
            self.page['首页']['应用按钮'].click()
            self.page['首页']['Telegram备份列表'].click()

        if self.page['首页']['备份按钮'].wait(3):
            self.page['首页']['备份按钮'].click()
            time.sleep(2)
            for _ in range(60):
                if not self.page['首页']['正在备份弹窗'].exists:
                    # print('备份成功')
                    return True  # 备份成功
                time.sleep(1)

    def restorApp(self, app_name):
        self.page['首页']['备份/还原'].click()
        time.sleep(.5)
        if self.page['首页']['Telegram备份列表'].exists:
            self.page['首页']['Telegram备份列表'].click()
        else:
            self.page['首页']['点击编辑过滤器'].click()
            self.adbInputText(self.page['首页']['编辑框'],
                              app_name,
                              delete=True,
                              del_num=10)
            self.page['首页']['应用按钮'].click()
            self.page['首页']['Telegram备份列表'].click()
        time.sleep(1)
        if self.page['首页']['备份按钮'].wait(3):
            if self.page['首页']['恢复按钮'].exists:  # 存在备份
                self.page['首页']['恢复按钮'].click()
                self.page['首页']['恢复-数据按钮'].click()
                time.sleep(1)
                if self.page['首页']['app正在运行提示'].exists:
                    self.page['首页']['确定结束按钮'].click()
                    time.sleep(1)
                for _ in range(60):
                    if not self.page['首页']['正在恢复弹窗'].exists:
                        # print('恢复成功')
                        return True
            else:
                print('不存在备份文件')
                return

    # 使用adb输入内容
    def adbInputText(self, el, text, delete=False, del_num=5):
        el.click()
        if delete:
            for _ in range(del_num):
                self.d.press('delete')
        self.ld.adbInputText(text)


class YYBL(object):
    """应用变量"""
    def __init__(self, ip, ld):
        self.ip = ip
        self.ld = ld
        self.packagename = 'com.sollyu.xposed.hook.model'
        self.d = u2.connect(self.ip)
        self.page = self.uiDict()

    def uiDict(self):
        page = {}
        page['首页'] = {}
        page['首页']['menu'] = self.d.xpath(
            '//*[@resource-id="com.sollyu.xposed.hook.model:id/button_menu"]')
        page['首页']['Telegram'] = self.d.xpath('//*[@text="Telegram"]')
        page['首页']['选项按钮'] = self.d.xpath(
            '//*[@resource-id="com.sollyu.xposed.hook.model:id/floatingActionMenu"]/android.widget.ImageButton[1]'
        )
        page['首页']['选项按钮-隐藏'] = self.d.xpath(
            '//*[@resource-id="com.sollyu.xposed.hook.model:id/floatingActionMenu"]/android.widget.ImageButton[7]'
        )
        page['首页']['全部执行'] = self.d.xpath('//*[@text="全部执行"]')
        page['首页']['全部随机'] = self.d.xpath('//*[@text="全部随机"]')
        page['首页']['运行程序'] = self.d.xpath('//*[@text="运行程序"]')
        page['首页']['强制停止'] = self.d.xpath('//*[@text="强制停止"]')
        page['首页']['清空应用'] = self.d.xpath('//*[@text="清空应用"]')
        page['首页']['保存配置'] = self.d.xpath('//*[@text="保存配置"]')
        page['首页']['返回按钮'] = self.d.xpath(
            '//*[@resource-id="com.sollyu.xposed.hook.model:id/button_back"]')
        page['首页']['参数列表'] = self.d.xpath(
            '//*[@resource-id="com.sollyu.xposed.hook.model:id/groupListView"]/android.widget.RelativeLayout'
        )
        page['首页']['厂商'] = self.d.xpath(
            '//android.widget.TextView[@text="厂商"]')
        page['首页']['厂商Box'] = self.d.xpath(
            '//android.widget.TextView[@text="厂商"]/following-sibling::android.widget.EditText'
        )
        page['首页']['选项列表'] = self.d.xpath(
            '//*[@resource-id="com.sollyu.xposed.hook.model:id/listview"]')
        page['首页']['列表'] = self.d.xpath(
            '//*[@resource-id="com.sollyu.xposed.hook.model:id/listview"]/android.widget.LinearLayout'
        )
        page['首页']['型号列表'] = self.d.xpath(
            '//*[@resource-id="com.sollyu.xposed.hook.model:id/listview"]/android.widget.LinearLayout'
        )
        page['首页']['型号'] = self.d.xpath(
            '//android.widget.TextView[@text="型号"]')
        page['首页']['型号Box'] = self.d.xpath(
            '//android.widget.TextView[@text="型号"]/following-sibling::android.widget.EditText'
        )
        page['首页']['序号'] = self.d.xpath(
            '//android.widget.TextView[@text="序号"]')
        page['首页']['序号Box'] = self.d.xpath(
            '//android.widget.TextView[@text="序号"]/following-sibling::android.widget.EditText'
        )
        page['首页']['版本'] = self.d.xpath(
            '//android.widget.TextView[@text="版本"]')
        page['首页']['版本Box'] = self.d.xpath(
            '//android.widget.TextView[@text="版本"]/following-sibling::android.widget.EditText'
        )
        page['首页']['手机号'] = self.d.xpath(
            '//android.widget.TextView[@text="手机号"]')
        page['首页']['手机号Box'] = self.d.xpath(
            '//android.widget.TextView[@text="手机号"]/following-sibling::android.widget.EditText'
        )
        page['首页']['网络类型'] = self.d.xpath(
            '//android.widget.TextView[@text="网络类型"]')
        page['首页']['网络类型Box'] = self.d.xpath(
            '//android.widget.TextView[@text="网络类型"]/following-sibling::android.widget.EditText'
        )
        page['首页']['IMEI'] = self.d.xpath(
            '//android.widget.TextView[@text="IMEI"]')
        page['首页']['IMEIBox'] = self.d.xpath(
            '//android.widget.TextView[@text="IMEI"]/following-sibling::android.widget.EditText'
        )
        page['首页']['IMSI'] = self.d.xpath(
            '//android.widget.TextView[@text="IMSI"]')
        page['首页']['IMSIBox'] = self.d.xpath(
            '//android.widget.TextView[@text="IMSI"]/following-sibling::android.widget.EditText'
        )
        page['首页']['SIM厂商'] = self.d.xpath('//*[@text="SIM厂商"]')
        page['首页']['SIM厂商BOX'] = self.d.xpath(
            '//*[@text="SIM厂商"]/following-sibling::android.widget.EditText')
        page['首页']['SIM国际'] = self.d.xpath(
            '//android.widget.TextView[@text="SIM国际"]')
        page['首页']['SIM国际Box'] = self.d.xpath(
            '//android.widget.TextView[@text="SIM国际"]/following-sibling::android.widget.EditText'
        )
        page['首页']['SIM名称'] = self.d.xpath(
            '//android.widget.TextView[@text="SIM名称"]')
        page['首页']['SIM名称Box'] = self.d.xpath(
            '//android.widget.TextView[@text="SIM名称"]/following-sibling::android.widget.EditText'
        )
        page['首页']['SIM序号'] = self.d.xpath(
            '//android.widget.TextView[@text="SIM序号"]')
        page['首页']['SIM序号Box'] = self.d.xpath(
            '//android.widget.TextView[@text="SIM序号"]/following-sibling::android.widget.EditText'
        )
        page['首页']['SIM状态'] = self.d.xpath(
            '//android.widget.TextView[@text="SIM状态"]')
        page['首页']['SIM状态Box'] = self.d.xpath(
            '//android.widget.TextView[@text="SIM状态"]/following-sibling::android.widget.EditText'
        )
        page['首页']['无线名称'] = self.d.xpath(
            '//android.widget.TextView[@text="无线名称"]')
        page['首页']['无线名称Box'] = self.d.xpath(
            '//android.widget.TextView[@text="无线名称"]/following-sibling::android.widget.EditText'
        )
        page['首页']['无线BSSID'] = self.d.xpath(
            '//android.widget.TextView[@text="无线BSSID"]')
        page['首页']['无线BSSIDBox'] = self.d.xpath(
            '//android.widget.TextView[@text="无线BSSID"]/following-sibling::android.widget.EditText'
        )
        page['首页']['无线MAC'] = self.d.xpath(
            '//android.widget.TextView[@text="无线MAC"]')
        page['首页']['无线MACBox'] = self.d.xpath(
            '//android.widget.TextView[@text="无线MAC"]/following-sibling::android.widget.EditText'
        )
        page['首页']['语言'] = self.d.xpath(
            '//android.widget.TextView[@text="语言"]')
        page['首页']['语言Box'] = self.d.xpath(
            '//android.widget.TextView[@text="语言"]/following-sibling::android.widget.EditText'
        )
        page['首页']['AndroidID'] = self.d.xpath(
            '//android.widget.TextView[@text="AndroidID"]')
        page['首页']['AndroidIDBox'] = self.d.xpath(
            '//android.widget.TextView[@text="AndroidID"]/following-sibling::android.widget.EditText'
        )
        page['首页']['UserAgent'] = self.d.xpath(
            '//android.widget.TextView[@text="UserAgent"]')
        page['首页']['UserAgentBox'] = self.d.xpath(
            '//android.widget.TextView[@text="UserAgent"]/following-sibling::android.widget.EditText'
        )
        page['首页']['MarkItem'] = self.d.xpath(
            '//*[@resource-id="com.sollyu.xposed.hook.model:id/bottom_dialog_list_item_mark"]'
        )
        page['首页']['随机'] = self.d.xpath(
            '//*[@resource-id="com.sollyu.xposed.hook.model:id/bottom_dialog_list_item_title"]'
        )
        return page

    def startApp(self):
        self.d.app_stop(self.packagename)
        time.sleep(1)
        self.ld.runApp(self.packagename)
        for _ in range(10):
            if self.page['首页']['menu'].exists:
                # print('启动成功')
                return True

    def startTelegram(self, phone=None):
        self.tg = Telegram(self.ip, self.ld)

        self.d.app_stop(self.tg.packagename)
        time.sleep(1)
        self.d.app_clear(self.tg.packagename)
        self.page['首页']['Telegram'].click()
        # self.page['首页']['选项按钮'].click()
        # time.sleep(1)
        # if self.page['首页']['全部随机'].exists:
        #     self.page['首页']['全部随机'].click()
        #     time.sleep(1)
        # self.page['首页']['选项按钮-隐藏'].click()
        # time.sleep(1)
        device_dict = self.setParam(phone)
        self.page['首页']['选项按钮'].click()
        self.page['首页']['保存配置'].click()
        time.sleep(.5)
        self.page['首页']['运行程序'].click()
        time.sleep(3)
        if device_dict:
            return device_dict

    def setParam(self, phone=None):
        try:
            pdict = {}
            if self.page['首页']['厂商'].wait():
                self.page['首页']['厂商'].click()
                time.sleep(.5)
                for _ in range(2):
                    if self.page['首页']['列表'].exists:
                        els = self.page['首页']['列表'].all()
                        if els:
                            random.choice(els).click()
                    time.sleep(1)

                pdict['厂商'] = self.page['首页']['厂商Box'].info['text']
                pdict['型号'] = self.page['首页']['型号Box'].info['text']
            # 点击序号
            pdict['序号'] = ''.join(
                random.choice(string.digits + string.ascii_lowercase)
                for _ in range(16))

            self.page['首页']['序号Box'].set_text(pdict['序号'])
            version = '{}.{}.{}'.format(random.randint(1, 9),
                                        random.randint(1, 9),
                                        random.randint(1, 9))
            self.page['首页']['版本Box'].set_text(version)
            pdict['版本'] = version
            # 输入手机号
            if not phone:
                phone = ''.join(
                    random.choice(string.digits) for _ in range(10))
                phone = '+1{}'.format(phone)
            self.page['首页']['手机号Box'].set_text(phone)
            pdict['手机号'] = phone
            # 输入网络类型
            self.page['首页']['网络类型Box'].set_text(random.choice(['wifi', '13']))
            pdict['网络类型'] = self.page['首页']['网络类型Box'].info['text']
            # 输入IMEI
            pdict['IMEI'] = ''.join(
                random.choice(string.digits) for _ in range(15))
            self.page['首页']['IMEIBox'].set_text(pdict['IMEI'])
            # 输入IMSI
            pdict['IMSI'] = ''.join(
                random.choice(string.digits) for _ in range(15))
            self.page['首页']['IMSIBox'].set_text(pdict['IMSI'])
            # 输入SIM信息
            moblie_dict = {
                'AT&T': 383,
                'Boost': 628,
                'Altice Mobile': 11359,
                'Nemont CDMA': 796,
                'T-Mobile': 79,
                'Union Telephone': 549,
                'Verizon': 77,
                'Cellcom': 587
            }
            pdict['SIM名称'] = random.choice([
                'AT&T', 'Boost', 'Altice Mobile', 'Nemont CDMA', 'T-Mobile',
                'Union Telephone', 'Verizon', 'Cellcom'
            ])
            mobile_name = pdict['SIM名称']
            pdict['SIM厂商'] = str(moblie_dict[mobile_name])
            self.page['首页']['SIM厂商BOX'].set_text(pdict['SIM厂商'])
            self.page['首页']['SIM国际Box'].set_text('us')
            self.page['首页']['SIM名称Box'].set_text(pdict['SIM名称'])
            pdict['SIM序号'] = ''.join(
                random.choice(string.digits) for _ in range(16))
            self.page['首页']['SIM序号Box'].set_text(pdict['SIM序号'])
            self.d.swipe_ext("up")
            self.d.swipe_ext("up", scale=0.5)
            pdict['SIM状态'] = '5'
            self.page['首页']['SIM状态Box'].set_text(pdict['SIM状态'])
            pdict['无线名称'] = "{}_{}".format(
                random.choice(['Tenda', 'TP-LINK', 'MERCURY', 'ASUS', 'FAST']),
                ''.join(
                    random.choice(string.digits + string.ascii_uppercase)
                    for _ in range(5)))

            self.page['首页']['无线名称Box'].set_text(pdict['无线名称'])
            ks = []
            for _ in range(5):
                k = ''.join(
                    random.choice(string.digits + string.ascii_uppercase)
                    for _ in range(2))
                ks.append(k)
            pdict['无线BSSID'] = func.createMac()
            self.page['首页']['无线BSSIDBox'].set_text(pdict['无线BSSID'])
            ks = []
            for _ in range(5):
                k = ''.join(
                    random.choice(string.digits + string.ascii_uppercase)
                    for _ in range(2))
                ks.append(k)
            pdict['无线MAC'] = func.createMac()
            self.page['首页']['无线MACBox'].set_text(pdict['无线MAC'])
            pdict['语言'] = 'en_US'
            self.page['首页']['语言Box'].set_text(pdict['语言'])
            pdict['AndroidID'] = ''.join(
                random.choice(string.digits + string.ascii_lowercase)
                for _ in range(16))
            self.page['首页']['AndroidIDBox'].set_text(pdict['AndroidID'])
            pdict[
                'UserAgent'] = 'Mozilla/5.0 (Linux; Android {}; G8141 Build/KG4NGO) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.4057.34 Mobile Safari/537.36'.format(
                    pdict['版本'])
            self.page['首页']['UserAgentBox'].set_text(pdict['UserAgent'])

            return pdict
        except Exception as e:
            print(str(e))
            return

    def startAppByTxt(self, app_name, txt):
        print(txt)
        if os.path.exists(txt):
            li = func.ReadTxt(txt)
            if li:
                content = li[0].replace('\'', '"')
                dic = func.str2json(content)
                if dic:
                    self.ld.killApp(self.packagename)
                    # 启动应用变量
                    self.startApp()
                    # 进入telegram
                    self.page['首页']['Telegram'].click()
                    self.page['首页']['返回按钮'].wait()
                    # 设置参数
                    for k, v in dic.items():
                        print(k, v)
                        if k == '厂商':
                            self.page['首页']['厂商Box'].set_text(v)
                        if k == '型号':
                            self.page['首页']['型号Box'].set_text(v)
                        if k == '序号':
                            self.page['首页']['序号Box'].set_text(v)
                        if k == '版本':
                            self.page['首页']['版本Box'].set_text(v)
                        if k == '手机号':
                            self.page['首页']['手机号Box'].set_text(v)
                        if k == '网络类型':
                            self.page['首页']['网络类型Box'].set_text(v)
                        if k == 'IMEI':
                            self.page['首页']['IMEIBox'].set_text(v)
                        if k == 'IMSI':
                            self.page['首页']['IMSIBox'].set_text(v)
                        if k == 'SIM厂商':
                            self.page['首页']['SIM厂商BOX'].set_text(v)
                        if k == 'SIM国际':
                            self.page['首页']['SIM国际Box'].set_text(v)
                        if k == 'SIM名称':
                            self.page['首页']['SIM名称Box'].set_text(v)
                        if k == 'SIM序号':
                            self.page['首页']['SIM序号Box'].set_text(v)
                            self.d.swipe_ext("up")
                            self.d.swipe_ext("up", scale=0.5)
                        if k == 'SIM状态':
                            self.page['首页']['SIM状态Box'].set_text(v)
                        if k == '无线名称':
                            self.page['首页']['无线名称Box'].set_text(v)
                        if k == '无线BSSID':
                            self.page['首页']['无线BSSIDBox'].set_text(v)
                        if k == '无线MAC':
                            self.page['首页']['无线MACBox'].set_text(v)
                        if k == '语言':
                            self.page['首页']['语言Box'].set_text(v)
                        if k == 'AndroidID':
                            self.page['首页']['AndroidIDBox'].set_text(v)
                        if k == 'UserAgent':
                            self.page['首页']['UserAgentBox'].set_text(v)
                    # 启动telegram
                    self.page['首页']['选项按钮'].click()
                    self.page['首页']['保存配置'].click()
                    self.page['首页']['运行程序'].click()
        else:  # 文件不存在
            return


class WhatsApp(object):
    def __init__(self, emu):
        super().__init__()
        self.emu = emu  # 模拟器
        self.local_ip = self.emu.local_ip  # 局域网ip
        self.d = u2.connect(self.local_ip)  # 需要先启动atx-agent服务
        self.d.implicitly_wait(10)  # 元素隐式等待
        self.package_name = 'com.whatsapp'
        self.data_path = '/data/data/com.whatsapp'
        self.page = self.ui_dict()

    def ui_dict(self):
        page = {}
        page['reg'] = {}
        page['reg']['agree_and_continue'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/eula_accept"]')
        page['reg']['country'] = self.d.xpath(
            '//android.widget.EditText[@resource-id="com.whatsapp:id/registration_cc"]'
        )
        page['reg']['phone_number'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/registration_phone"]')
        page['reg']['next'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/registration_submit"]')
        page['reg']['invailid_phone'] = self.d.xpath(
            '//*[@resource-id="android:id/message" and contains(@text, "is not a valid mobile number")]'
        )
        page['reg']['ok_btn'] = self.d.xpath(
            '//android.widget.Button[@text="OK"]')
        page['reg']['input_code'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/verify_sms_code_input"]')
        page['reg']['resend_btn'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/resend_sms_btn"]')
        page['reg']['code_failed'] = self.d.xpath(
            '//*[@resource-id="android:id/message" and contains(@text, "The code you entered is incorrect")]'
        )
        page['reg']['countdown_time_sms'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/countdown_time_sms"]'
        )  # 重新发送的等待时间
        page['reg']['cannot_sms'] = self.d.xpath('//android.widget.TextView[@resource-id="android:id/message" and contains(@text , "We couldn\'t send an SMS to your number")]')
        page['reg']['google_drive_backup_tips'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/permission_message" and contains(@text, "To find and restore your backup from Google Drive")]'
        )
        page['reg']['cancel_btn'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/cancel"]')
        page['reg']['submit_btn'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/submit"]')
        page['reg']['registration_name'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/registration_name"]')
        page['reg']['register_name_accept'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/register_name_accept"]')
        page['reg']['change_photo_btn'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/change_photo_btn"]')
        page['reg']['gallery_btn'] = self.d.xpath('//*[@text="Gallery"]')
        page['reg']['access_media_tips'] = self.d.xpath(
            '//android.widget.TextView[@resource-id="com.android.packageinstaller:id/permission_message" and contains(@text, "Allow WhatsApp to access photos")]'
        )
        page['reg']['temporarily_unavailable'] = self.d.xpath('//android.widget.TextView[contains(@text, "WhatsApp is temporarily unavailable")]')
        page['reg']['deny_btn'] = self.d.xpath(
            '//*[@resource-id="com.android.packageinstaller:id/permission_deny_button"]'
        )
        page['reg']['allow_btn'] = self.d.xpath(
            '//*[@resource-id="com.android.packageinstaller:id/permission_allow_button"]'
        )
        page['reg']['albums'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/albums"]')
        page['reg']['album_grid'] = self.d.xpath('//*[@resource-id="com.whatsapp:id/grid"]')
        page['reg']['photo'] = self.d.xpath('//*[@content-desc="Photo"]')
        page['reg']['all_photos'] = self.d.xpath('//android.widget.TextView[contains(@text,"All photos")]')
        page['reg']['change_photo_progress'] = self.d.xpath('//*[@resource-id="com.whatsapp:id/change_photo_progress"]')
        page['reg']['ok_btn_down'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/ok_btn"]')
        page['reg']['verify_phone'] = self.d.xpath(
            '//android.widget.TextView[contains(@text, "verify your phone number to log back into your account")]'
        )
        page['reg']['verify_btn'] = self.d.xpath(
            '//android.widget.Button[@text="VERIFY"]')

        page['index'] = {}
        page['index']['chats'] = self.d.xpath('//*[@text="CHATS"]')
        page['index']['button_open_permission_settings'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/button_open_permission_settings"]'
        )
        page['index']['new_chat'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/fab" and @content-desc="New chat"]'
        )
        page['index']['contact_tips'] = self.d.xpath(
            '//*[@resource-id="com.whatsapp:id/permission_message" and contains(@text, "To help you message friends and family on WhatsApp")]'
        )
        page['index']['permissions_btn'] = self.d.xpath(
            '//*[@text="Permissions"]')

        page['permissions'] = {}
        page['permissions']['page_sign'] = self.d.xpath(
            '//android.widget.TextView[@text="App permissions"]')
        page['permissions']['off'] = self.d.xpath(
            '//android.widget.Switch[@text="OFF"]')
        return page

    def reg_account(self, country, phone, get_code=lambda: input('reg code:')):
        try:
            self.emu.kill_app(self.package_name)  # kill app
            self.emu.clear_app(self.package_name)  # clear app data

            self.d.app_start(self.package_name)
            self.page['reg']['agree_and_continue'].click_exists()
            if self.page['reg']['country'].wait():
                self.page['reg']['country'].set_text(country)
                self.page['reg']['phone_number'].set_text(phone)
                self.page['reg']['next'].click()
            if self.page['reg']['ok_btn'].wait(
                    10):  # number is ok, click ok button
                if self.page['reg'][
                        'invailid_phone'].exists:  # invalid phone , return and change new phone number
                    self.page['reg']['ok_btn'].click()
                    return
                else:  # valid phone number, continue
                    self.page['reg']['ok_btn'].click()
                    if self.page['reg']['input_code'].wait(
                            10):  # input reg code
                        code = get_code()
                        if code:
                            self.page['reg']['input_code'].set_text(code)
                            if self.page['reg']['code_failed'].wait(1):
                                self.page['reg']['ok_btn'].click()
                                return
                        else: 
                            return
            # whatsapp 被临时禁止, 结束注册任务
            if self.page['reg']['temporarily_unavailable'].wait(2):
                return
            if self.page['reg']['google_drive_backup_tips'].wait(
                    2):  # google drive backup tips , click cancel
                self.page['reg']['cancel_btn'].click()

            # set nickname and choice avatar
            if self.page['reg']['registration_name'].wait(5):
                # input nickame
                nickname = self.emu.faker.name() or 'cuckootool'
                self.page['reg']['registration_name'].set_text(nickname)
                # change photo
                self.page['reg']['change_photo_btn'].click_exists()
                self.page['reg']['gallery_btn'].click_exists()
                if self.page['reg']['access_media_tips'].wait(3):
                    self.page['reg']['allow_btn'].click()
                time.sleep(3)
                if self.page['reg']['all_photos'].exists:
                    self.page['reg']['all_photos'].click_exists(1)
                    time.sleep(2)
                    images = self.page['reg']['album_grid'].child('/android.widget.ImageView').all()
                else:
                    images = self.page['reg']['albums'].child(
                        '/android.widget.FrameLayout').all()
                if images:
                    images_count = len(images)
                    index = random.randint(0, images_count)
                    images[index].click()
                    self.page['reg']['photo'].click_exists()
                    time.sleep(2)
                    self.page['reg']['ok_btn_down'].click_exists()
                    time.sleep(10)  # wait for photo uploaded
                else:
                    pass
                    # album have not image , need upload images
                self.back2el(self.page['reg']['register_name_accept'])
                self.page['reg']['register_name_accept'].click_exists()

            els = [self.page['index']['chats'], self.page['reg']['verify_phone']]
            if self.wait_els(els, 180):
                if self.page['index']['chats'].exists:
                    if self.page['reg']['verify_phone'].wait(20):
                        self.page['reg']['verify_btn'].click()
                        return
                    return True
                if self.page['reg']['verify_phone'].exists:
                    self.page['reg']['verify_btn'].click()
                    return
                time.sleep(1)

        except Exception as e:
            print(str(e))
            pass

    def set_permissions(self):
        if self.page['index']['button_open_permission_settings'].exists:
            self.page['index']['button_open_permission_settings'].click()
            if self.page['index']['contact_tips'].wait(3):
                self.page['reg']['submit_btn'].click_exists()
            # set permissions page
            self.page['index']['permissions_btn'].click_exists()
            if self.page['permissions']['page_sign'].wait(5):
                off_btns = self.page['permissions']['off'].all()
                if off_btns:
                    for btn in off_btns:
                        btn.click()
                        time.sleep(.5)
                if self.back_index():
                    return True

    def set_device(self):
        resp = self.emu.getprop()
        print(resp)

    def back_index(self):
        """back to index page"""
        for _ in range(5):
            if self.page['index']['chats'].exists:
                return True
            else:
                self.d.press('back')
                time.sleep(1)

    def back2el(self, xth):
        for _ in range(5):
            if xth.exists:
                return True
            else:
                self.d.press('back')
                time.sleep(1)

    
    def wait_els(self, els, t=10):
        for _ in range(t):
            if type(els)==str:
                if els.exists:
                    return True
            elif type(els)==list:
                for el in els:
                    if el.exists:
                        return True
            time.sleep(1)

class Twitter(object):
    def __init__(self, emu):
        super().__init__()
        self.emu = emu  # 模拟器
        self.local_ip = self.emu.local_ip  # 局域网ip
        self.d = u2.connect(self.local_ip)  # 需要先启动atx-agent服务
        self.d.implicitly_wait(10)  # 元素隐式等待
        self.package_name = 'com.twitter.android'
        self.data_path = '/data/data/com.twitter.android'
        self.page = self.ui_dict()

    def ui_dict(self):
        pass


class TikTok(object):
    def __init__(self) -> None:
        super().__init__()
        self.package_name = 'com.zhiliaoapp.musically'