#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests, re, time, json, threading, os
import urllib3
import urllib.request

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import mod.func as func



def HttpGet(url, headers=None, t=10):
    try:
        if headers is None:
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }
        html = requests.get(url, headers=headers, timeout=t)
        if html.status_code == 200:  # 验证成功
            html_str = html.text
            if html_str:
                return html_str
        else:
            pass
            # print(html.status_code, html.text)
    except Exception as e:
        func.err_log("HttpGet:{}".format(str(e)))
        return


def HttpPost(url, data, headers=None, t=10):
    try:
        if headers is None:
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }
        if type(data) != str:
            data = json.dumps(data)
        html = requests.post(url, data=data, headers=headers, timeout=t)
        # print(type(data))
        # print(str(html))
        # print(html.status_code,html.text)
        if html.status_code == 200:  # 验证成功
            html_str = html.text
            if html_str:
                return html_str
        else:
            print(html.status_code, html.text)
    except Exception as e:
        print(e)
        return


def HttpPatch(url, data, headers=None, t=10):
    try:
        if headers is None:
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }
        if type(data) != str:
            data = json.dumps(data)
        html = requests.patch(url, data=data, headers=headers, timeout=t)
        # print(type(data))
        # print(str(html))
        # print(html.status_code,html.text)
        if html.status_code == 200:  # 验证成功
            html_str = html.text
            if html_str:
                return html_str
        else:
            print(html.status_code, html.text)
    except Exception as e:
        print(e)
        return


def HttpRequest(url, data, rtype='put', headers=None, t=10, proxy_dict=None):
    try:
        if headers is None:
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }
        if type(data) != str:
            data = json.dumps(data)
        if rtype == 'put':
            html = requests.put(url,
                                data=data,
                                headers=headers,
                                timeout=t,
                                proxies=proxy_dict)
        elif rtype == 'get':
            html = requests.get(url,
                                headers=headers,
                                timeout=t,
                                proxies=proxy_dict)
        elif rtype == 'patch':
            html = requests.patch(url,
                                  data=data,
                                  headers=headers,
                                  timeout=t,
                                  proxies=proxy_dict)
        elif rtype == 'delete':
            html = requests.delete(url,
                                   data=data,
                                   headers=headers,
                                   timeout=t,
                                   proxies=proxy_dict)
        elif rtype == 'post':
            html = requests.post(url,
                                 data=data,
                                 headers=headers,
                                 timeout=t,
                                 proxies=proxy_dict)
        return html
    except Exception as e:
        # print(e)
        func.err_log("HttpRequest:" + str(e))
        return


"""
   手机验证码函数, 包括获取号码, 获取信息 等
"""


# 获取token
def Koko_GetToken(user, password):
    url = "http://dkh.hfsxf.com:81/service.asmx/UserLoginStr?name=%s&psw=%s" % (
        user, password)
    return HttpGet(url)


# 获取号码
def Koko_GetPhone(token, pid):
    url = "http://dkh.hfsxf.com:81/service.asmx/GetHM2Str?token=%s&xmid=%s&sl=1&lx=0&a1=&a2=&pk=&ks=0&rj=0" % (
        token, pid)
    resp = HttpGet(url)
    # print(resp)
    if resp:
        phone = re.search(r'\d+', resp)
        if phone:
            phone = phone.group()
            return phone


# 获取短信
def Koko_GetSms(token, phone, pid):
    url = 'http://dkh.hfsxf.com:81/service.asmx/GetYzm2Str?token=%s&hm=%s&xmid=%s&sf=1' % (
        token, phone, pid)
    for i in range(0, 10):
        msg = HttpGet(url)
        # print(msg)
        if msg and len(msg) > 4:
            mcs = re.findall(r'\d+', msg)
            code = None
            for mc in mcs:
                if not code:
                    code = mc
                else:
                    if len(mc) > len(code):
                        code = mc
                        return code
        elif msg == '-8':
            print("帐户余额不足")
            return
        else:
            print(phone + " have no message , waitng 5 sec " + str(i) +
                  ' time ')
            time.sleep(5)


# 释放号码
def Koko_ReleasePhone(token, phone):
    url = 'http://dkh.hfsxf.com:81/service.asmx/sfHmStr?token=%s&hm=%s' % (
        token, phone)
    HttpGet(url)


# 卡码多 获取token
def Kmd_GetToken(user, password):
    url = "http://api.178kmd.cn/api/login?userName=%s&password=%s" % (user,
                                                                      password)
    resp = HttpGet(url)
    if resp:
        token = re.search(r'.*\|(.*)', resp).group(1)
        return token


# 卡码多 获取号码
def Kmd_GetPhone(token, pid):
    """
    成功响应示例
    0|手机号|运营商|省份|城市
    示例：0|13000000000|中国移动|山东|济南
    失败响应示例
    1|错误信息
    示例：1|暂时没有可用号码
    """
    url = "http://api.178kmd.cn/api/getPhone?sid=%s&token=%s&developer=pagelist" % (
        pid, token)
    resp = HttpGet(url)
    # print(resp)
    if resp:
        return resp
        # mc=re.search(r'0\|(\d+)',resp)
        # if mc:
        #    phone=mc.group(1)
        #    if phone:
        #       return phone


# 卡码多获取短信
def Kmd_GetSms(token, phone, pid):
    url = "http://api.178kmd.cn/api/getMessage?sid=%s&phone=%s&token=%s" % (
        pid, phone, token)
    for i in range(0, 30):
        msg = HttpGet(url)
        if msg and len(msg) > 4:
            mcs = re.findall(r'\d+', msg)
            code = None
            for mc in mcs:
                if not code:
                    code = mc
                else:
                    if len(mc) > len(code):
                        code = mc
                        print(phone, '获取验证码成功:', code)
                        return code
        print(phone, '获取验证码%s次,等待5秒' % str(i))
        # print(phone+" have no message , waitng 5 sec " + str(i)+ ' time ')
        time.sleep(5)


# 卡码多释放号码
def Kmd_ReleasePhone(token, phone, pid):
    url = "http://api.178kmd.cn/api/cancelRecv?sid=%s&phone=%s&token=%s" % (
        pid, phone, token)
    return HttpGet(url)


# 卡码多 拉黑号码
def Kmd_BannePhone(pid, phone, token):
    url = 'http://api.178kmd.cn/api/addBlacklist?sid=%s&phone=%s&token=%s' % (
        pid, phone, token)
    return HttpGet(url)


def Sms_activate_token(token=None):
    if token is None:
        # token="464f2027Ad46322065e981b468791102"
        token = '755289d553004e08A65084359c3c89ce'
    return token


def Sms_activate_Phone(token, pid="tg", country=None):
    try:
        # host="http://43.239.159.124"
        host = "https://sms-activate.ru"
        # token=Sms_activate_token()
        url = "%s/stubs/handler_api.php?api_key=%s&action=getNumber&service=%s&ref=244691&country=%s" % (
            host, token, pid, country)
        resp = HttpGet(url)
        # print(resp)
        res_dict = {}
        if resp:
            if "ACCESS_NUMBER" in resp:
                # mc=re.compile(r"(\d+):(\d+)")
                mr = re.search(r"(\d+):(\d+)", resp)
                if mr:
                    res_dict['phone'] = mr.group(2)
                    res_dict['tid'] = mr.group(1)
                # print(res_dict)
                return res_dict
            else:
                # print(resp)
                return
    except Exception as e:
        func.err_log("Sms_activate_Phone:{}".format(str(e)))


def Sms_activate_SetStatus(status, tid, token=None):
    try:
        # host="http://43.239.159.124"
        host = "https://sms-activate.ru"
        if token is None:
            token = Sms_activate_token()
        url = "%s/stubs/handler_api.php?api_key=%s&action=setStatus&status=%s&id=%s" % (
            host, token, status, tid)
        resp = HttpGet(url)
        # print(resp)
        if resp:
            return resp
    except Exception as e:
        func.err_log("Sms_activate_SetStatus:{}".format(str(e)))


def Sms_activate_GetStatus(phone, tid, token):
    try:
        # if token is None:
        #    token=Sms_activate_token()
        # host="http://43.239.159.124"
        host = "https://sms-activate.ru"
        url = "%s/stubs/handler_api.php?api_key=%s&action=getStatus&id=%s" % (
            host, token, tid)
        # print(url)
        for _ in range(7):
            resp = HttpGet(url)
            if resp:
                # print(resp)
                if "STATUS_OK" in resp:
                    code = re.search(r"\d{5,}", resp).group()
                    # print('%s获取验证码成功:%s'% (phone,code))
                    return code
                else:
                    # print('%s获取验证码%s次,等待5秒' % (phone,str(i)))
                    time.sleep(5)
                    # func.Waiting(5)
    except Exception as e:
        func.err_log("Sms_activate_GetStatus:{}".format(str(e)))


# 项目报价
def Sms_activate_GetPrice(pid, country=None, token=None):
    try:
        if token is None:
            token = Sms_activate_token()
        host = "https://sms-activate.ru"
        if country is None:
            country_str = ""
        else:
            country_str = "&country=" + country
        url = "%s/stubs/handler_api.php?api_key=%s&action=getPrices&service=%s%s" % (
            host, token, pid, country_str)
        # print(url)
        resp = HttpGet(url)
        if resp:
            return resp
    except Exception as e:
        func.err_log("Sms_activate_GetPrice:{}".format(str(e)))


# 私密平台
def Private1_GetCode(url, token=None, phone=None, num=10):
    if token:
        if 'http' in token:
            url = token
        else:
            url = "%s%s" % (url, token)
    # print(url)
    for _ in range(num):
        try:
            resp = HttpRequest(url, None, rtype='get')
            print(url)
            print(resp.text)
            if resp.status_code == 200:
                # print('http success',resp.text)
                mc = re.search(r"\d{5,}", resp.text)
                if mc:
                    code = mc.group()
                    if code:
                        # print('%s获取验证码成功:%s'% (phone,code))
                        return code
            # print('%s获取验证码%s次,等待5秒' % (phone,str(i)))
            time.sleep(5)
        except Exception as e:
            func.err_log("private code:" + str(e))


# www.5sim.net
class FiveSimClass(object):
    def __init__(self, token):
        super().__init__()
        self.token = token

        self.service = 'telegram'

    def httpget(self, url):
        try:
            headers = {'Authorization': 'Bearer {}'.format(self.token)}
            html = requests.get(url, headers=headers, timeout=30)
            if html.status_code == 200:  # 验证成功
                html_str = html.text
                if html_str:
                    return html_str
            else:
                print(html.status_code, html.text)
        except Exception as e:
            # print(str(e))
            func.err_log('FiveSimClass-http:{}'.format(str(e)))
            return

    def get_balance(self):
        url = "https://5sim.net/v1/user/profile"
        resp = self.httpget(url)
        if resp:
            return resp

    def get_phone(self, country):
        url = "https://5sim.net/v1/user/buy/activation/{}/any/telegram".format(
            country)
        resp = self.httpget(url)
        if resp:
            rdict = func.str2json(resp)
            if rdict:
                return rdict

    def get_code(self, order_id):
        url = "https://5sim.net/v1/user/check/{}".format(order_id)
        for _ in range(7):
            resp = self.httpget(url)
            if resp:
                rdict = func.str2json(resp)
                if rdict and rdict['status'] == 'RECEIVED' and len(
                        rdict['sms']) > 0 and rdict['sms'][0]['code']:
                    code = rdict['sms'][0]['code']
                    return code
            time.sleep(5)

    def finish_order(self, order_id):
        url = "https://5sim.net/v1/user/finish/{}".format(order_id)
        resp = self.httpget(url)
        if resp:
            rdict = func.str2json(resp)
            if rdict:
                return rdict

    def cancel_order(self, order_id):
        url = "https://5sim.net/v1/user/cancel/{}".format(order_id)
        resp = self.httpget(url)
        if resp:
            rdict = func.str2json(resp)
            if rdict:
                return rdict

    def ban_order(self, order_id):
        url = "https://5sim.net/v1/user/ban/{}".format(order_id)
        resp = self.httpget(url)
        if resp:
            rdict = func.str2json(resp)
            if rdict:
                return rdict


# 柠檬国际 http://www2.smspva.net/
class NmgjClass(object):
    def __init__(self, username, password):
        super().__init__()
        self.username, self.password = username, password
        self.pid = '0257'  # 项目id, telegram

    def get_balance(self):
        url = "http://opapi.smspva.net/out/ext_api/getUserInfo?name={}&pwd={}".format(
            self.username, self.password)
        resp = HttpGet(url)
        if resp:
            rdict = func.str2json(resp)
            if rdict:
                return rdict

    def get_phone(self, country):
        url = "http://opapi.smspva.net/out/ext_api/getMobile?name={}&pwd={}&cuy={}&pid={}&num=1&noblack=1".format(
            self.username, self.password, country, self.pid)
        resp = HttpGet(url)
        if resp:
            rdict = func.str2json(resp)
            if rdict and rdict['code'] == 200:
                return rdict

    def get_code(self, phone):
        if '+' in phone:
            phone = phone.replace('+', '')
        url = "http://opapi.smspva.net/out/ext_api/getMsg?name={}&pwd={}&pn=+{}&pid={}".format(
            self.username, self.password, phone, self.pid)

        for _ in range(7):
            resp = HttpGet(url)
            if resp:
                rdict = func.str2json(resp)
                if rdict and rdict['code'] == 200:
                    _data = rdict['data']
                    mc = re.search(r"\d{5,}", _data)
                    if mc:
                        code = mc.group()
                        return code
            time.sleep(5)

    def release_number(self, phone):
        url = "http://opapi.smspva.net/out/ext_api/passMobile?name={}&pwd={}&pn=+{}&pid={}&serial=1".format(
            self.username, self.password, phone, self.pid)
        resp = HttpGet(url)
        return resp

    def ban_number(self, phone):
        url = "http://opapi.smspva.net/out/ext_api/addBlack?name={}&pwd={}&pn=+{}&pid={}".format(
            self.username, self.password, phone, self.pid)
        resp = HttpGet(url)
        return resp

    def check_number(self, phone):
        if '+' in phone:
            phone = phone.replace('+', '')
        url = "http://opapi.smspva.net/out/ext_api/getStatus?name={}&pwd={}&pn=+{}&pid={}".format(
            self.username, self.password, phone, self.pid)
        resp = HttpGet(url)
        return resp

    def check_number_in_blacklist(self, phone):
        if '+' in phone:
            phone = phone.replace('+', '')
        url = "http://opapi.smspva.net/out/ext_api/getBlack?name={}&pwd={}&pn=+{}&pid={}".format(
            self.username, self.password, phone, self.pid)
        resp = HttpGet(url)
        return resp


# Jindou平台 http://www.jindousms.com/
class JindouClass(object):
    def __init__(self, token):
        super(JindouClass, self).__init__()
        self.token = token

    def get_number(self, pid, country_id, proxy):
        try:
            if not country_id:
                country_id = ''
            url = 'http://www.jindousms.com/public/sms/getNumber?myPid={}&locale={}&apikey={}'.format(
                pid, country_id, self.token)
            if proxy:
                proxy = {"http": proxy, "https": proxy}
                resp = requests.get(url, timeout=30, proxies=proxy)
            else:
                resp = requests.get(url, timeout=30)
            if resp and resp.status_code == 200:
                rdict = func.str2json(resp.text)
                if rdict:
                    return rdict
        except Exception as e:
            func.err_log(str(e))

    def get_code(self, order_id, proxy):
        try:
            if proxy:
                proxy = {"http": proxy, "https": proxy}
            url = 'http://www.jindousms.com/public/sms/getCode?orderId={}&apikey={}'.format(
                order_id, self.token)
            for _ in range(7):
                if proxy:
                    resp = requests.get(url, timeout=30, proxies=proxy)
                else:
                    resp = requests.get(url, timeout=30)
                if resp and resp.status_code == 200:
                    rdict = func.str2json(resp.text)
                    if rdict and rdict['code'] == 1:
                        code = rdict['data']['code']
                        return code
                time.sleep(5)
        except Exception as e:
            func.err_log('Jindou get code error: {}'.format(str(e)))

    def release_phone(self, order_id, proxy):
        if proxy:
            proxy = {"http": proxy, "https": proxy}
        url = 'http://www.jindousms.com/public/sms/releaseNumber?orderId={}&apikey={}'.format(
            order_id, self.token)
        if proxy:
            resp = requests.get(url, timeout=30, proxies=proxy)
        else:
            resp = requests.get(url, timeout=30)
        if resp and resp.status_code == 200:
            rdict = func.str2json(resp.text)
            if rdict:
                return rdict

    def blacklist_phone(self, order_id, proxy):
        if proxy:
            proxy = {"http": proxy, "https": proxy}
        url = 'http://www.jindousms.com/public/sms/shieldNumber?orderId={}&apikey={}'.format(
            order_id, self.token)
        if proxy:
            resp = requests.get(url, timeout=30, proxies=proxy)
        else:
            resp = requests.get(url, timeout=30)
        if resp and resp.status_code == 200:
            rdict = func.str2json(resp)
            if rdict:
                return rdict


# SMS-MAN平台 https://sms-man.com/  UUbim8WDrym9S4od95b2QIvva3c5NUFc
class SMS_MAN_CLASS(object):
    def __init__(self, token) -> None:
        super().__init__()
        self.token = token

    def get_banlance(self, proxy=None):
        url = 'http://api.sms-man.ru/stubs/handler_api.php?action=getBalance&api_key={}'.format(
            self.token)
        if proxy:
            proxy = {"http": proxy, "https": proxy}
            resp = requests.get(url, timeout=30, proxies=proxy)
        else:
            resp = requests.get(url, timeout=30)
        if resp and resp.status_code == 200:
            rdict = resp.text
            if rdict:
                return rdict

    def get_all_counties(self, proxy=None):
        """获取所有国家列表, 返回list"""
        url = 'http://api.sms-man.ru/stubs/handler_api.php?action=getCountries&api_key={}'.format(
            self.token)
        if proxy:
            proxy = {"http": proxy, "https": proxy}
            resp = requests.get(url, timeout=30, proxies=proxy)
        else:
            resp = requests.get(url, timeout=30)
        if resp and resp.status_code == 200:
            rdict = resp.text
            if rdict:
                try:
                    new_list = json.loads(rdict)
                except:
                    new_list = None
                finally:
                    return new_list

    def get_service_number(self, country=187, service='tg', proxy=None):
        """获取项目号码价格和数量. [返回dict]"""
        url = 'http://api.sms-man.ru/stubs/handler_api.php?action=getPrices&api_key={}&country={}&service={}'.format(
            self.token, country, service)
        if proxy:
            proxy = {"http": proxy, "https": proxy}
            resp = requests.get(url, timeout=30, proxies=proxy)
        else:
            resp = requests.get(url, timeout=30)
        if resp and resp.status_code == 200:
            rdict = resp.text
            if rdict:
                rdict = func.str2json(rdict)
                return rdict

    def get_phone(self, service='tg', country=187, proxy=None):
        try:
            url = 'http://api.sms-man.ru/stubs/handler_api.php?action=getNumber&api_key={}&service={}&country={}&ref=hk3keQJImN6R'.format(
                self.token, service, country)
            if proxy:
                proxy = {"http": proxy, "https": proxy}
                resp = requests.get(url, timeout=30, proxies=proxy)
            else:
                resp = requests.get(url, timeout=30)
            if resp and resp.status_code == 200:
                rdict = resp.text
                # print(url, rdict)
                if rdict and 'ACCESS_NUMBER' in rdict:  # ACCESS_NUMBER:$id:$number
                    l = rdict.split(':')
                    if l:
                        rdict = {'id': l[1], 'phone': l[2]}
                    return rdict
        except Exception as e:
            func.err_log(str(e))

    def get_status(self, phone_id, proxy=None):
        # """
        # STATUS_WAIT_CODE - waiting for sms
        # STATUS_WAIT_RETRY:$lastcode - waiting for code refinement (where is $lastcode, inappropriate code)
        # STATUS_WAIT_RESEND - if you selected retry sms set status to 6
        # STATUS_CANCEL - activation rejected
        # STATUS_OK:$smscode - $smscode is your sms code for registration
        # """
        try:
            url = 'http://api.sms-man.ru/stubs/handler_api.php?action=getStatus&api_key={}&id={}'.format(
                self.token, phone_id)
            if proxy:
                proxy = {"http": proxy, "https": proxy}
                resp = requests.get(url, timeout=30, proxies=proxy)
            else:
                resp = requests.get(url, timeout=30)
            if resp and resp.status_code == 200:
                rdict = resp.text
                if rdict:  # STATUS_OK:$smscode - $smscode is your sms code for registration
                    return rdict
        except Exception as e:
            func.err_log(str(e))

    def get_code(self, phone_id, proxy=None):
        """获取验证码"""
        for _ in range(7):
            resp = self.get_status(phone_id, proxy=proxy)
            if 'STATUS_OK' in resp:
                mc = re.search(r"\d{5,}", resp)
                if mc:
                    code = mc.group()
                    return code
            time.sleep(5)

    def change_status(self, phone_id, status, proxy=None):
        """修改订单状态"""
        # """
        # -1 - reject activation
        # 1 - report availability (sms has been sent)
        # 3 - request another sms (free)
        # 6 - complete activation (if status "sms received" - complete activation successfully, if status "waiting retry" changes activation to get a new sms code)
        # 8 - number used or banned
        # """
        try:
            url = 'http://api.sms-man.ru/stubs/handler_api.php?action=setStatus&api_key={}&id={}&status={}'.format(
                self.token, phone_id, status)
            if proxy:
                proxy = {"http": proxy, "https": proxy}
                resp = requests.get(url, timeout=30, proxies=proxy)
            else:
                resp = requests.get(url, timeout=30)
            if resp and resp.status_code == 200:
                rdict = resp.text
                if rdict:
                    return rdict
        except Exception as e:
            func.err_log(str(e))


class DataServer(object):
    """api接口数据,上传dict(必须包括action),返回dict(包含action,resp,status,err,more,sign)"""
    def __init__(self):
        super().__init__()
        # port=8443 # 如通过cf则必须使用指定端口, 否则数据有可能不能通过cf
        # self.url = 'https://api.wuya88.com/api'  # 测试环境
        self.url = 'https://api2.wuya88.com/api'  # 正式环境

    def http(self, post_data, timeout=60):
        try:
            sign = None
            if type(post_data) == dict:
                sign = func.str2Md5(
                    func.RandomStr(7))  # http请求签名, 返回要核对,一致说明返回正确
                post_data['sign'] = sign
                post_data = func.json2str(post_data)
            else:
                post_data = str(post_data)
            # print('post_data',post_data)
            if type(post_data) == str:
                post_data = func.super_en(post_data)
            # print('post_data', post_data)
            resp = requests.post(self.url, post_data, timeout=timeout)
            # print('resp', resp)
            if resp:
                resp_text = resp.text

                resp_text = func.super_de(resp_text)
                if resp_text:
                    resp_dict = func.str2json(resp_text)
                    if resp_dict:
                        if sign and resp_dict['sign'] == sign:
                            # print('resp_dict',resp_dict)
                            return resp_dict
        except Exception as e:
            # print(str(e))
            func.err_log('DataServer http:{}'.format(str(e)))

    # 上传硬件日志
    def upload_device_log(
        self,
        task_class,
        action,
        log_dict,
        device,
        ip,
    ):
        # 上传日志
        try:
            log_str = func.json2str(log_dict)
            if not log_str:
                log_str = ''
            device_log = {
                'class': task_class,
                'action': 'device_log',
                'device': device,
                'ac': action,
                'ip': ip,
                'log': log_str
            }
            self.upload_th = threading.Thread(target=self.http,
                                              args=(
                                                  device_log,
                                                  30,
                                              ))
            self.upload_th.start()
            # self.http(device_log,timeout=30)
        except:
            pass

def get_mcc_mnc():
    """获取移动通信商的mcc和mnc信息"""
    td_re = re.compile('<td>([^<]*)</td>'*6)
    with urllib.request.urlopen('http://mcc-mnc.com/') as f:
        html = f.read().decode('utf-8')
        tbody_start = False
        mcc_mnc_list = []
        for line in html.split('\n'):
            if '<tbody>' in line:
                tbody_start = True
            elif '</tbody>' in line:
                break
            elif tbody_start:
                td_search = td_re.search(line)
                current_item = {}
                td_search = td_re.split(line)
                current_item['mcc'] = td_search[1]
                current_item['mnc'] = td_search[2]
                current_item['iso'] = td_search[3]
                current_item['country'] = td_search[4]
                current_item['country_code'] = td_search[5]
                current_item['network'] = td_search[6][0:-1]
                mcc_mnc_list.append(current_item)
        print(json.dumps(mcc_mnc_list, indent=2))
        db = 'mcc.db'
        if os.path.exists(db):
            try:
                os.remove(db)
            except:
                pass

def get_mcc_dict(country_code, mcc_file='mcc.txt'):
    # 获取mcc
    # mcc_file = 'mcc.txt'
    if not os.path.exists(mcc_file):
        get_mcc_mnc()
    mcc_list = func.ReadTxt(mcc_file)
    if mcc_list and type(mcc_list)==list:
        mcc_list = json.loads(mcc_list[0])
    # 筛选指定国家的mcc
    if mcc_list:
        region_mcc_list = []
        for mcc in mcc_list:
            if mcc['iso'] == country_code.lower():
                region_mcc_list.append(mcc)
        return region_mcc_list