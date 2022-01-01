import time, base64, pyDes, json, hashlib, os, http.client, psutil, signal, chardet, string, random, re, shutil, \
    datetime, sys, socks, socket, requests, functools, logging, traceback, telethon
from py7zr import pack_7zarchive, unpack_7zarchive
import subprocess
from subprocess import Popen, PIPE

from pypinyin import lazy_pinyin

if sys.platform == 'win32':
    import win32api

    pass


# byte转str
def byte2str(_byte):
    st = None
    try:
        st = str(_byte, encoding='gbk')
    except:
        pass
    if not st:
        try:
            st = str(_byte, encoding='utf-8')
        except:
            pass
    if not st:
        try:
            st = str(_byte, encoding='unicode_escape')
        except:
            pass
    return st


# 按照长度分割字符
def splitStrByLen(st, lenth):
    st2 = re.findall(r'.{' + str(lenth) + '}', st)
    if st2:
        return st2
    else:
        return


def getDeviceMd5():
    if sys.platform == 'win32':
        cv = win32api.GetVolumeInformation('c:\\')[1]
        if cv:
            return hashlib.md5(str(cv).encode('utf8')).hexdigest()


# 暂定 等待
def Waiting(t=10, st=''):
    for i in range(t):
        print('%swaiting %s' % (st, str(t - i)))
        time.sleep(1)


def RandomUsername(num=8):
    zm = string.ascii_lowercase
    sz = string.digits
    zms = ''.join(random.choice(zm) for _ in range(3))
    szs = ''.join(random.choice(sz) for _ in range(num - 3))
    username = zms + szs
    return username


# 随机中文
def GBK2312(num=1):
    ss = ""
    for _ in range(num):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xfe)
        val = f'{head:x}{body:x}'
        ss = ss + str(bytes.fromhex(val).decode('gb2312'))
    return ss


# 随机大小写字母/数字 [len:长度; repeat:是否重复字符, 默认fasle 不重复]
def RandomStr(len, repeat=False):
    if repeat:
        random_str = ''.join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(len))
    else:
        random_str = ''.join(
            random.sample(string.ascii_letters + string.digits, len))
    return random_str


def randomNickname():
    cn_num = random.randint(1, 2)
    cn = GBK2312(cn_num)
    # print(cn)
    first_name = ''.join(lazy_pinyin(cn))
    last_name = ''.join(lazy_pinyin(GBK2312(1)))
    return first_name, last_name


# ?????? (??)
def Unicode(num=1):
    ss = ""
    for _ in range(num):
        val = random.randint(0x4e00, 0x9fbf)
        ss = ss + str(chr(val))
    return ss


def GetRectXY(rect):
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]
    x, y = rect[0] + int(w / 2), rect[1] + int(h / 2)
    return x, y


# des 加密
def DesEncrypt(data, key='5EC9E222', iv='F1C15925'):
    method = pyDes.des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    k = method.encrypt(data)
    return base64.b64encode(k)


# des 解密
def DesDecrypt(data, key='5EC9E222', iv='F1C15925'):
    method = pyDes.des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    k = base64.b64decode(data)
    return method.decrypt(k)


# 栅栏W字符
def generate_w(string, n):
    """将字符排列成w型"""
    array = [['.'] * len(string) for i in range(n)]  # 生成初始矩阵
    row = 0
    upflag = False
    for col in range(len(string)):  # 在矩阵上按w型画出string
        array[row][col] = string[col]
        if row == n - 1:
            upflag = True
        if row == 0:
            upflag = False
        if upflag:
            row -= 1
        else:
            row += 1
    return array


# 栅栏w加密
def zl_encode(string, n):
    """加密"""
    array = generate_w(string, n)
    msg = []
    for row in range(n):  # 将每行的字符连起来
        for col in range(len(string)):
            if array[row][col] != '.':
                msg.append(array[row][col])
    return ''.join(msg)
    # return array, msg


# 栅栏w解密
def zl_decode(string, n):
    """解密"""
    array = generate_w(string, n)
    sub = 0
    for row in range(n):  # 将w型字符按行的顺序依次替换为string
        for col in range(len(string)):
            if array[row][col] != '.':
                array[row][col] = string[sub]
                sub += 1
    msg = []
    for col in range(len(string)):  # 以列的顺序依次连接各字符
        for row in range(n):
            if array[row][col] != '.':
                msg.append(array[row][col])
    # return array, msg
    return ''.join(msg)


# 超级加密
def super_en(st):
    key = "WXCZXF84"
    iv = 'WXLWM116'
    try:
        method = pyDes.des(key,
                           pyDes.CBC,
                           iv,
                           pad=None,
                           padmode=pyDes.PAD_PKCS5)
        k = method.encrypt(st)
        k = base64.b64encode(k)
        k = k.decode()
        # 栅栏加密
        zl = random.randint(2, int(len(k) / 2))
        scode = "{}{}".format(len(str(zl)), zl)
        k = zl_encode(k, zl)
        if len(k) > 7:
            k_list = list(k)
            k_list.insert(7, scode)
            k = ''.join(k_list)
        return k
    except Exception as e:
        # print('super_en',str(e))
        return


# 超级解密
def super_de(st):
    key = "WXCZXF84"
    iv = 'WXLWM116'
    try:
        if len(st) > 7:
            k_list = list(st)
            index = int(k_list[7])
            le = 8 + int(index)
            zl = ''.join(k_list[8:le])
            del k_list[7:le]
            st = ''.join(k_list)
            zl = int(zl)
            st = zl_decode(st, zl)
            if st:
                method = pyDes.des(key,
                                   pyDes.CBC,
                                   iv,
                                   pad=None,
                                   padmode=pyDes.PAD_PKCS5)
                k = base64.b64decode(st)
                k = method.decrypt(k)
                k = k.decode()
                return k
    except Exception as e:
        # print(str(e))
        return


# 超级加密
def log_encrypt(st):
    key = "WXLSOGEN"
    iv = 'CJLJILZD'
    try:
        method = pyDes.des(key,
                           pyDes.CBC,
                           iv,
                           pad=None,
                           padmode=pyDes.PAD_PKCS5)
        k = method.encrypt(st)
        k = base64.b64encode(k)
        k = k.decode()
        # 栅栏加密
        zl = random.randint(2, int(len(k) / 2))
        scode = "{}{}".format(len(str(zl)), zl)
        k = zl_encode(k, zl)
        if len(k) > 7:
            k_list = list(k)
            k_list.insert(7, scode)
            k = ''.join(k_list)
        return k
    except Exception as e:
        # print('super_en',str(e))
        return


# 超级解密
def log_decrypt(st):
    key = "WXLSOGEN"
    iv = 'CJLJILZD'
    try:
        if len(st) > 7:
            k_list = list(st)
            index = int(k_list[7])
            le = 8 + int(index)
            zl = ''.join(k_list[8:le])
            del k_list[7:le]
            st = ''.join(k_list)
            zl = int(zl)
            st = zl_decode(st, zl)
            if st:
                method = pyDes.des(key,
                                   pyDes.CBC,
                                   iv,
                                   pad=None,
                                   padmode=pyDes.PAD_PKCS5)
                k = base64.b64decode(st)
                k = method.decrypt(k)
                k = k.decode()
                return k
    except Exception as e:
        # print(str(e))
        return


def decrpyt_session(session_str):
    """解密session.[session_str: session加密串.][返回:dict,{'session_str':'string','device':{}}]"""
    session_dict = {}
    key = 'EAC5645A'
    iv = '3B27DBD7'
    try:
        session_dict = {}
        session_str = bytes(session_str, encoding='utf-8')

        method = pyDes.des(key,
                           pyDes.CBC,
                           iv,
                           pad=None,
                           padmode=pyDes.PAD_PKCS5)
        # k = base64.b64decode(session_str)
        k = base64_decode(session_str)
        st = method.decrypt(k)
        st = st.decode()  # byte转字符
        try:
            ss = eval(st)  # 如果正常eval表示为老旧格式, 如果报错则判断是base64格式,需要base64解码
            st = ss
        except:
            # st = base64_2str(st)  # base64 解密, 解决特殊字符的加密失败的问题
            st = base64_decode(st)
            st = eval(st)

        st = json.dumps(st)  # 兼容单引号json字符
        session_dict = str2json(st)
    except Exception as e:
        # print(str(e))
        session_dict = {"session_str": session_str, "device": {}}
    finally:
        if session_dict and type(session_dict['session_str']) == bytes:
            session_dict['session_str'] = session_dict['session_str'].decode()
        return session_dict


def encrypt_session(session_dict):
    """加密session[session_dict: session表, 包括session字符串和硬件信息. {'session_str':'string','device':{}}][返回:str 加密后的session字符串]"""
    try:
        key = 'EAC5645A'
        iv = '3B27DBD7'
        session_str = str(session_dict)
        b64 = str2base64(session_str)  # base64加密, 避免特殊字符导致加密失败
        method = pyDes.des(key,
                           pyDes.CBC,
                           iv,
                           pad=None,
                           padmode=pyDes.PAD_PKCS5)
        # k = method.encrypt(session_str)
        k = method.encrypt(b64)
        session_str = base64.b64encode(k)
        session_str = session_str.decode()
        return session_str
    except Exception as e:
        err_log('encrypt_session:{}'.format(str(e)))


def getDmi():
    p = Popen(['dmidecode'], stdout=PIPE)
    data = p.stdout.read()
    return data


def getUUID():
    _data = str(getDmi())
    _list = _data.split('\\n')
    if _list:
        dmi_list = list(filter(None, _list))
    for line in dmi_list:
        line = line.replace('\t', '')
        if 'UUID' in line and not 'None' in line:
            mc = re.search(r'UUID: (.*)', line)
            if mc:
                uuid = mc.group(1)
            else:
                uuid = line
            return uuid


def GetDeviceMd5():
    if sys.platform == 'win32':
        cv = win32api.GetVolumeInformation('c:\\')[1]
        if cv:
            return hashlib.md5(str(cv).encode('utf8')).hexdigest()
    elif sys.platform == 'linux':
        # dmi = dmidecode.DMIDecode()
        # cv=dmi.serial_number()
        cv = getUUID()
        if cv:
            hd = hashlib.md5(str(cv).encode('utf8')).hexdigest()
            return hd


# 根据机器码,生成指定有效期的注册码 =====================================================
def MakeVcode(device, softname, day=31, loop=7, k_class=None):
    try:
        info = {}
        info['softname'] = softname
        info['device'] = device
        info['time'] = int(time.time() + day * 60 * 60 * 24)
        if k_class and type(
                k_class) == str and '{' in k_class and "}" in k_class:
            d = json.loads(k_class)
        if k_class and type(k_class) == dict:
            d = k_class
        for key, value in d.items():
            d[key] = (value * (60 * 60 * 24)) + time.time()
        info['k_class'] = d
        vcode = DesEncrypt(json.dumps(info)).decode('utf8')
        if loop > 0 and vcode:
            for _ in range(loop):
                vcode = DesEncrypt(vcode).decode('utf8')
        # print(vcode)
        return vcode
    except:
        return


# json转字符串
def json2str(j):
    try:
        return json.dumps(j)
    except:
        return None


def str2json(st):
    try:
        _dict = json.loads(st)
        if _dict and type(_dict) == dict:
            return _dict
    except:
        return None


# 获取网络时间戳
def GetWebTimestamp(host='www.baidu.com'):
    for _ in range(3):
        try:
            conn = http.client.HTTPSConnection(host, timeout=3)
            conn.request("GET", "/")
            r = conn.getresponse()
            # r.getheaders() #获取所有的http头
            ts = r.getheader('date')  # 获取http头date部分
            # print(ts)
            # print(ts[5:25])
            timestamp = int(
                time.mktime(
                    datetime.datetime.strptime(
                        ts[5:25], r"%d %b %Y %H:%M:%S").timetuple()))

            # # 将GMT时间转换成北京时间
            # ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
            # print(ltime)
            # timestamp=int(time.mktime(ltime) + 8 * 60 * 60)
            # print(timestamp)
            return timestamp
        except Exception as e:
            print(e)


# string 按转/分割成list
def Str2List(string, spl="\n"):
    l = string.split(spl)
    if l:
        d = list(filter(None, l))
        return d


# list 按照指定字符分割成更小的list
def ListSplit(l, spl='========'):
    full_l = []
    sl = []
    for s in l:
        if spl in s:
            full_l.append(sl)
            sl = []
        else:
            pass
            sl.append(s)
    if sl:
        full_l.append(sl)
    return full_l


# txt读取为list
def ReadTxt(txtfile):
    file = txtfile
    txtlist = []
    try:
        if file and os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    for line in lines:
                        line = line.strip("\n")
                        txtlist.append(line)
    except:
        pass
    return txtlist


# 检查txt文档编码
def CheckTxtCode(file):
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']


def WriteTxt(file, content, mode='wb+', delete=None):
    try:
        dirname = os.path.dirname(file)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        if delete:
            delete_file(file)
        with open(file, mode) as f:
            content = content + '\n'
            if mode == 'wb+':
                f.write(content.encode('utf-8'))
            else:
                f.write(content)
    except Exception as e:
        err_log(str(e))
    finally:
        pass


# 将list写入txt文档 (覆盖)
def write_list_txt(file, wlist, delete=None):
    try:
        # 生成目录
        dirname = os.path.dirname(file)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        if delete:
            delete_file(file)
            time.sleep(.5)
        filename = open(file, 'w', encoding='utf-8')
        wlist = [line + "\n" for line in wlist]
        filename.writelines(wlist)
    except Exception as e:
        err_log(str(e))
    finally:
        filename.close()


# 添加内容到txt (行尾添加, 非覆盖)
def add_txt(file, content):
    try:
        # 生成目录
        dirname = os.path.dirname(file)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(file, 'a+', encoding='utf-8') as f:
            f.write(str(content) + '\n')  # 加\n换行显示
    except Exception as e:
        err_log(str(e))
    finally:
        f.close()


# 添加list到文件
def add_list_txt(file, ls):
    try:
        dirname = os.path.dirname(file)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        ls = [str(j) + '\n' for j in ls]
        with open(file, 'a+', encoding='utf-8') as f:
            f.writelines(ls)
    except Exception as e:
        err_log(str(e))
    finally:
        f.close()


def err_log(log):
    """写入错误日志[msg:日志内容]返回:无"""
    try:
        file = 'err.log'
        if os.path.exists(file) and os.path.getsize(
                file) > 100 * 1024:  # 判断文件大小, 超过100k就删除
            os.remove(file)
        log = get_time_str() + " : " + log
        trace = str(traceback.format_exc())
        trace = log_encrypt(trace)
        log = '{}\n{}'.format(log, trace)
        WriteTxt(file, log, mode='a+')
        WriteTxt(
            file,
            "============================================================================================",
            mode='a+')
    finally:
        pass


def str_include_list(str, list):
    """
   字符串中包含列表中的指定字符
   """
    for l in list:
        if l in str:
            return True


# 更新dict值 , 主要解决manager.dict() 无法更新值的问题
def dict_update(d, k, v):
    dd = d
    if type(k) == list and type(v) == list and len(k) == len(v):
        for i in range(len(k)):
            index = k[i]
            dd[index] = v[i]
    else:
        dd[k] = v
    d = dd
    return d


def proxy_str2proxy_dict(proxy_str):
    """代理字符串转代理字典, 如:sock5://127.0.0.1:10808 转 {socks5:127.0.0.1:10808} . 用于request代理功能使用"""
    proxy_str = proxy_str.replace('socks5', 'socks5h')
    proxies = {'http': proxy_str, 'https': proxy_str}
    return proxies


# 获取当前时间, 返回时间字符串 2020-10-04 03:57:18
def get_time_str():
    """
   获取当前时间, 返回时间字符串 2020-10-04 03:57:18
   """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 数字型时间戳转换为年月日字符格式
def timestamp2time(timestamp):
    """数字型时间戳转换为年月日字符格式"""
    if not type(timestamp) == int:
        timestamp = int(timestamp)
    if timestamp:
        # 转换成localtime
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt


# 修改文件md5
def change_md5(file):
    try:
        writefile = int(time.time() * 1000)
        with open(file, "a") as f:
            f.write(str(writefile))
    except:
        pass


# 获取文件md5
def get_md5(file_path):
    md5 = None
    if os.path.isfile(file_path):
        f = open(file_path, 'rb')
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
        return md5


# 删除文件
def delete_file(file):
    if os.path.exists(file):
        try:
            os.remove(file)
            return True
        except Exception as e:
            err_log(str(e))


# 字符转md5
def str2Md5(st):
    md5 = hashlib.md5()
    md5.update(st.encode('utf-8'))
    return md5.hexdigest()


# 字符串转base64字符串
def str2base64(st):
    """字符串转base64字符串"""
    # st_bytes = st.encode('ascii')
    st_bytes = st.encode('utf-8')
    b64 = base64.b64encode(st_bytes)
    return b64.decode()


# base64字符串解密为字符串
def base64_2str(b64_str):
    """base64字符串解密为字符串"""
    # b64=b64_str.encode()
    b64_str = base64.b64decode(b64_str)
    return b64_str.decode()


def base64_decode(b64_str):
    try:
        b64_str = base64_2str(b64_str)
        return b64_str
    except Exception as e:
        # print(str(e))
        missing_padding = 4 - len(b64_str) % 4
        if missing_padding:
            b64_str += b'=' * missing_padding
        b64_str = base64.b64decode(b64_str)
        return b64_str


# tgtool commond语句
def tgtool_command(sql_id, dbfile):
    # tgtool='TgTool.exe'
    # command='%s %s %s' % (tgtool,sql_id,dbfile) # 程序
    # command="python tgtool.py %s %s " % (sql_id,dbfile) # 命令
    # return command
    pass
    return


# 汉字转拼音
def cn2py(cn):
    st = lazy_pinyin(cn)
    if st:
        return ''.join(st)
    else:
        return cn


# 获取随机用户名, 拼音_数字
def get_username():
    try:
        cn_num = random.randint(1, 4)
        cn = GBK2312(cn_num)
        # print(cn)
        cn_py = ''.join(lazy_pinyin(cn))
        if cn_py:
            fgf = ""
            if random.randint(1, 3) == 3:
                fgf = "_"
            if cn_num >= 3:
                cn_py = cn_py + fgf + str(random.randint(10, 999))
            else:
                cn_py = cn_py + fgf + str(random.randint(1000, 99999))
            # print(cn_py)
        return cn_py
        # type_list=[1,2,3]
        # for _ in range(100):
        #     username=''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA0123456789_',random.randint(5,8)))
        #     print(username)
    except:
        return


# 随机生成一个MAC地址的函数
def createMac():
    mac = [
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]
    return (':'.join(map(lambda x: "%02x" % x, mac))).upper()


# 复制临时图片,并更改图片md5值
def copy_tmp_img(pic):
    """复制临时图片,并更改图片md5值"""
    try:
        send_img = None
        if os.path.exists(pic):
            tmp_pic = 'tmp/%s_%s.jpg' % (random.randint(
                1, 999), random.randint(100000, 999999))
            shutil.copyfile(pic, tmp_pic)
            if os.path.exists(tmp_pic):
                change_md5(tmp_pic)
            send_img = tmp_pic
            return send_img
    except:
        return


def sql_dict(t):
    if t == 'init_db':
        create_dict = {}
        create_dict['config'] = """
      CREATE TABLE IF NOT EXISTS [config](
      [id] integer PRIMARY KEY autoincrement, 
      [status] INT NOT NULL DEFAULT 0, 
      [task] VARCHAR, 
      [key] VARCHAR, 
      [value] VARCHAR,
      [type] VARCHAR);
      """
        create_dict['log'] = """
      CREATE TABLE IF NOT EXISTS [log](
      [id] INTEGER PRIMARY KEY AUTOINCREMENT, 
      [status] INT NOT NULL DEFAULT 0, 
      [task] VARCHAR, 
      [aid]  INT DEFAULT 0,
      [phone] VARCHAR, 
      [action] VARCHAR, 
      [target] VARCHAR,
      [log] TEXT, 
      [result] TEXT,
      [more] TEXT,
      [pid] VARCHAR,
      [use_num] INT DEFAULT 0, 
      [yes] INT DEFAULT 0, 
      [no] INT DEFAULT 0, 
      [time] TIMESTAMP DEFAULT (datetime('now','localtime')));
      """
        # [time] TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        create_dict['task'] = """
      CREATE TABLE IF NOT EXISTS [task](
      [id] INTEGER PRIMARY KEY AUTOINCREMENT, 
      [status] INT DEFAULT 0, 
      [phone] VARCHAR, 
      [action] VARCHAR, 
      [target] VARCHAR,
      [log] TEXT, 
      [result] TEXT,
      [pid] VARCHAR,
      [more] TEXT,
      [use_num] INT DEFAULT 0, 
      [yes] INT DEFAULT 0, 
      [no] INT DEFAULT 0, 
      [time] TIMESTAMP DEFAULT (datetime('now','localtime')));
      """
        create_dict['user'] = """
      CREATE TABLE IF NOT EXISTS [user](
      [id] integer PRIMARY KEY autoincrement, 
      [status] INT DEFAULT 0, 
      [country] VARCHAR, 
      [phone] VARCHAR, 
      [api_id] VARCHAR, 
      [api_hash] VARCHAR, 
      [code] VARCHAR,
      [session] TEXT, 
      [proxy] VARCHAR,
      [pid] VARCHAR,
      [first_name] VARCHAR,
      [last_name] VARCHAR,
      [more] TEXT,
      [use_num] INT DEFAULT 0, 
      [yes] INT DEFAULT 0, 
      [no] INT DEFAULT 0, 
      [current_task] VARCHAR,
      [err] TEXT,
      [time] TIMESTAMP DEFAULT (datetime('now','localtime')));
      """
        create_dict['account'] = """
      CREATE TABLE IF NOT EXISTS [account](
      [id] integer PRIMARY KEY autoincrement, 
      [status] INT DEFAULT 0, 
      [type] VARCHAR,
      [task] VARCHAR,
      [country] VARCHAR, 
      [phone] VARCHAR, 
      [phone_str] VARCHAR, 
      [session] TEXT, 
      [api_id] VARCHAR, 
      [api_hash] VARCHAR, 
      [code] VARCHAR,
      [proxy] VARCHAR,
      [path] VARCHAR,
      [content] TEXT,
      [uid] VARCHAR,
      [username] VARCHAR,
      [password] VARCHAR,
      [first_name] VARCHAR,
      [last_name] VARCHAR,
      [device] VARCHAR,
      [data] TEXT,
      [more] TEXT,
      [pid] VARCHAR,
      [use_num] INT DEFAULT 0, 
      [yes] INT DEFAULT 0, 
      [no] INT DEFAULT 0, 
      [current_task] VARCHAR,
      [err] TEXT,
      [time] TIMESTAMP DEFAULT (datetime('now','localtime')));
      """
        create_dict['target'] = """
      CREATE TABLE IF NOT EXISTS [target](
      [id] integer PRIMARY KEY autoincrement, 
      [status] INT DEFAULT 0, 
      [type] VARCHAR,
      [task] VARCHAR, 
      [target] TEXT, 
      [data] TEXT,
      [more] TEXT,
      [pid] VARCHAR,
      [use_num] INT DEFAULT 0, 
      [yes] INT DEFAULT 0, 
      [no] INT DEFAULT 0, 
      [current_task] VARCHAR,
      [err] TEXT,
      [time] TIMESTAMP DEFAULT (datetime('now','localtime')));
      """
        create_dict['content'] = """
      CREATE TABLE IF NOT EXISTS [content](
      [id] integer PRIMARY KEY autoincrement, 
      [status] INT DEFAULT 0, 
      [type] VARCHAR,
      [task] VARCHAR,
      [user] VARCHAR, 
      [content] TEXT, 
      [other] TEXT,
      [more] TEXT,
      [pid] VARCHAR,
      [use_num] INT DEFAULT 0, 
      [yes] INT DEFAULT 0, 
      [no] INT DEFAULT 0, 
      [current_task] VARCHAR,
      [err] TEXT,
      [time] TIMESTAMP DEFAULT (datetime('now','localtime')));
      """
        create_dict['api'] = """
      CREATE TABLE IF NOT EXISTS [api](
      [id] integer PRIMARY KEY autoincrement, 
      [status] INT DEFAULT 0, 
      [api_id] VARCHAR,
      [api_hash] VARCHAR,
      [use_num] INT DEFAULT 0,
      [time] TIMESTAMP DEFAULT (datetime('now','localtime')));
      """
        create_dict['proxy'] = """
      CREATE TABLE IF NOT EXISTS [proxy](
      [id] integer PRIMARY KEY autoincrement, 
      [status] INT DEFAULT 0, 
      [task] VARCHAR,
      [proxy_str] TEXT, 
      [proxy_type] VARCHAR,
      [ip] VARCHAR,
      [port] VARCHAR,
      [more] TEXT,
      [use_num] INT DEFAULT 0, 
      [yes] INT DEFAULT 0, 
      [no] INT DEFAULT 0, 
      [time] TIMESTAMP DEFAULT (datetime('now','localtime')));
      """
        create_dict['collection'] = """
      CREATE TABLE IF NOT EXISTS [collection](
      [id] integer PRIMARY KEY autoincrement, 
      [status] INT DEFAULT 0, 
      [task] VARCHAR,
      [class] VARCHAR, 
      [type] VARCHAR, 
      [user] VARCHAR,
      [target] VARCHAR,
      [content] TEXT,
      [proxy] VARCHAR,
      [more] TEXT,
      [pid] VARCHAR,
      [use_num] INT DEFAULT 0, 
      [yes] INT DEFAULT 0, 
      [no] INT DEFAULT 0, 
      [time] TIMESTAMP DEFAULT (datetime('now','localtime')));
      """
        create_dict['dialog'] = """
      CREATE TABLE IF NOT EXISTS [dialog](
      [id] integer PRIMARY KEY autoincrement, 
      [status] INT DEFAULT 0, 
      [type] VARCHAR,
      [phone] VARCHAR,
      [me] VARCHAR,
      [user_id] VARCHAR,
      [username] VARCHAR,
      [user_phone] VARCHAR,
      [first_name] VARCHAR,
      [last_name] VARCHAR,
      [mutual_contact] INT DEFAULT 0,
      [more] TEXT,
      [pid] VARCHAR,
      [use_num] INT DEFAULT 0, 
      [yes] INT DEFAULT 0, 
      [no] INT DEFAULT 0, 
      [time] TIMESTAMP DEFAULT (datetime('now','localtime')));
      """
    elif t == 'creat_cdb':
        create_dict = {}
        create_dict['user'] = """
      CREATE TABLE IF NOT EXISTS [user](
      [id] integer PRIMARY KEY autoincrement, 
      [status] INT DEFAULT 0, 
      [task] VARCHAR,
      [class] VARCHAR, 
      [type] VARCHAR, 
      [user] VARCHAR,
      [target] VARCHAR,
      [proxy] VARCHAR,
      [uid] VARCHAR,
      [is_self] VARCHAR,
      [username] VARCHAR,
      [contact] VARCHAR,
      [mutual_contact] VARCHAR,
      [deleted] VARCHAR,
      [bot] VARCHAR,
      [bot_chat_history] VARCHAR,
      [bot_nochats] VARCHAR,
      [is_admin] VARCHAR,
      [verified] VARCHAR,
      [restricted] VARCHAR,
      [min] VARCHAR,
      [bot_inline_geo] VARCHAR,
      [support] VARCHAR,
      [scam] VARCHAR,
      [apply_min_photo] VARCHAR,
      [access_hash] VARCHAR,
      [first_name] VARCHAR,
      [last_name] VARCHAR,
      [phone] VARCHAR,
      [photo] VARCHAR,
      [user_status] VARCHAR,
      [join_time] VARCHAR,
      [bot_info_version] VARCHAR,
      [restriction_reason] VARCHAR,
      [bot_inline_placeholder] VARCHAR,
      [lang_code] VARCHAR,
      [more] TEXT,
      [pid] VARCHAR,
      [use_num] INT DEFAULT 0, 
      [yes] INT DEFAULT 0, 
      [no] INT DEFAULT 0, 
      [time] TIMESTAMP DEFAULT (datetime('now','localtime')));

      """
        create_dict['channel'] = """
      CREATE TABLE if not exists [channel](
      [id] integer PRIMARY KEY autoincrement, 
      [status] INT DEFAULT 0, 
      [task] VARCHAR,
      [class] VARCHAR, 
      [type] VARCHAR, 
      [keyword] VARCHAR,
      [user] VARCHAR,
      [target] VARCHAR,
      [proxy] VARCHAR,
      [uid] VARCHAR,
      [username] VARCHAR,
      [private_link] VARCHAR,
      [name] VARCHAR,
      [desc] VARCHAR,
      [admin] VARCHAR,
      [more] TEXT, 
      [pid] VARCHAR,
      [blob] BLOB,
      [use_num] INT DEFAULT 0, 
      [yes] INT DEFAULT 0, 
      [no] INT DEFAULT 0, 
      [time] TIMESTAMP DEFAULT (datetime('now','localtime')));
      """
    elif t == 'creat_session_db':
        create_dict = {}
        create_dict['version'] = """
      CREATE TABLE if not exists [version](
      [version] integer PRIMARY KEY)
      """
        create_dict['sessions'] = """
      CREATE TABLE if not exists [sessions](
      [dc_id] integer PRIMARY KEY, 
      [server_address] text, 
      [port] integer, 
      [auth_key] blob, 
      [takeout_id] integer)
      """
        create_dict['entities'] = """
      CREATE TABLE if not exists [entities](
      [id] integer PRIMARY KEY, 
      [hash] integer not null, 
      [username] text, 
      [phone] integer, 
      [name] text,
      [date] integer)
      """
        create_dict['sent_files'] = """
      CREATE TABLE if not exists [sent_files](
      [md5_digest] blob , 
      [file_size] integer, 
      [type] integer, 
      [id] integer, 
      [hash] integer,
      primary key(md5_digest, file_size, type))
      """
        create_dict['update_state'] = """
      CREATE TABLE if not exists [update_state](
      [id] integer PRIMARY KEY , 
      [pts] integer, 
      [qts] integer, 
      [date] integer, 
      [seq] integer)
      """

    return create_dict


def msg2cn(msg):
    if msg and type(msg) == str:
        if "you can't send media in this chat" in msg.lower():
            msg = '禁止发送图片/视频等'
        elif "you can't write in this chat" in msg.lower():
            msg = '此群/频道禁止发送消息'
        elif "The channel specified is private and you lack permission to access it. Another reason may be that you\
         were banned from it".lower() in msg:
            msg = '此群组/频道无法加入,或帐号已封禁'
        elif 'a wait of' in msg.lower() and 'seconds' in msg.lower():
            """
           A wait of 496 seconds is required before sending another message in this chat (caused by ForwardMessagesRequest)
           """
            mc = re.search(r'\d+', msg)
            if mc:
                sec = mc.group()
                msg = '帐号被禁言%s秒' % (sec)
        elif 'was used under two different IP addresses simultaneously' in msg:
            msg = '禁止session帐号同时在不同IP下使用'
        elif 'The used phone number has been banned from Telegram'.lower(
        ) in msg.lower():
            msg = '此号码已被封禁'
        elif 'deleted/deactivated' in msg.lower():
            msg = "Session已停用/掉线"
        elif 'banned from sending messages in supergroups' in msg.lower():
            msg = '禁止账号在此频道/群组中发送消息'
        elif 'Connection to Telegram failed'.lower() in msg.lower():
            msg = '代理IP/网络错误'
        elif 'consecutive sign-in attempts failed. Aborting'.lower(
        ) in msg.lower():
            msg = '多次获取验证码失败'
        elif 'The target user is not a member of the specified megagroup or channel'.lower(
        ) in msg.lower():
            msg = '该账号非群组/频道成员'
        elif "The user's privacy settings do not allow you to do this ".lower(
        ) in msg:
            msg = '用户的隐私设置不允许您执行此操作'
        elif 'Too many requests'.lower() in msg.lower():
            msg = "请求次数过多"
        elif 'No user has'.lower() in msg.lower() and 'as username'.lower(
        ) in msg.lower():
            msg = '用户不存在'
        elif 'Nobody is using this username, or the username is unacceptable'.lower(
        ) in msg.lower():
            msg = '帐号(对象)无效或无此账号(对象)'
        elif 'cannot find any entity'.lower() in msg.lower():
            msg = '对象不存在'
        elif 'You have joined too many channels/supergroups'.lower(
        ) in msg.lower():
            msg = '加入群(频道)太多/太频繁'
    return msg


def msg_type(msg):
    if msg:
        msg = msg.lower()
        resp = {
            'account_offline': [
                "deleted/deactivated",
                'The used phone number has been banned from Telegram'
            ],
            'ban_account': [
                "The channel specified is private and you lack permission to access it. Another reason may\
         be that you were banned from it",
                'banned from sending messages in supergroups',
                'Too many requests'
            ],
            'ban_proxy': ['Connection to Telegram failed'],
            'ban_user': [],
            'ban_content': [],
            'ban_target': [
                "you can't send media in this chat",
                "you can't write in this chat",
                'Nobody is using this username, or the username is unacceptable',
                ['No user has', 'as username'], 'cannot find any entity',
                'Nobody is using this username,\
                               or the username is unacceptable'
            ]
        }
        for k, v in resp.items():
            for m in v:
                if type(m) == str:  # 字符信息, m是否存在与msg中
                    if m.lower() in msg:
                        return k
                elif type(m) == list:  # list表示有多个字符需要判断, 判断list中的字符是否同时存在与msg中
                    in_msgs = []
                    for _m in m:
                        if _m.lower() in msg:
                            in_msgs.append(_m)
                    if in_msgs and in_msgs == m:
                        return k


def err_type2cn(err_type):
    """错误类型, 转成中文"""
    edict = {
        'UserDeactivatedBanError': '帐号已掉线/被封禁',
        'FloodWaitError': '被禁言或暂时封禁',
        'BotsTooMuchError': '此聊天/频道中有太多机器人。',
        'PeerFloodError': '洪水攻击警告',
        'UserBannedInChannelError': '您被禁止在超级组/频道中发送消息。',
        'UserBlockedError': '用户被阻止。',
        'BotGroupsBlockedError': '无法将此机器人添加到群组。',
        'ChannelInvalidError': '无效的频道对象。确保传递正确的类型，例如确保请求是为通道设计的，或者寻找更适合的不同类型。',
        'ChannelPrivateError': '指定的频道是私有的，您无权访问它。另一个原因可能是你被禁止了。',
        'ChannelsTooMuchError': '您加入的频道/超级组过 多.',
        'ChatAdminRequiredError':
        '在指定的聊天中执行此操作需要聊天管理员权限（例如，在不属于您的频道中发送消息），或用于 频道或群组的无效权限。',
        'ChatInvalidError': '此请求的聊天无效。',
        'ChatWriteForbiddenError': '你不能在这个聊天中写作。',
        'InputUserDeactivatedError': '指定的用户已被删除。',
        'UsersTooMuchError': '已超过最大用户数（例如创建聊天）。',
        'UserBotError': '机器人只能是频道中的管理员..',
        'UserChannelsTooMuchError': '您尝试添加的用户之一已经在太多频道/超级组中。',
        'UserIdInvalidError':
        '用户的对象 ID 无效。确保传递正确的类型，例如确保请求是为用户设计的，或者寻找更适合的不同类型。',
        'UserKickedError': '该用户被踢出这个超级组/频道。',
        'UserNotMutualContactError': '提供的用户不是相互联系的。',
        'UserPrivacyRestrictedError': '用户的隐私设置不允许您这样做。',
        'ValueError': '参数错误',
        'UsernameInvalidError': '无效的username',
        'ConnectionError': '客户端未连接',
        'AuthKeyDuplicatedError': 'session不能同时在两个不同的IP地址下使用',
        'BotDomainInvalidError': '用于身份验证按 钮的域与@BotFather 中配置的域不匹配。',
        'ButtonDataInvalidError': '提供的按钮数据无效。',
        'ButtonTypeInvalidError': '提供的其中一个按钮的类型无效。',
        'ButtonUrlInvalidError': '按钮 URL 无效。',
        'ChatIdInvalidError': '无效的聊天对象 ID。',
        'ChatRestrictedError': '聊天受到限制，不能在该请求中使用。',
        'EntitiesTooLongError': '不再可能在实体标签内发送如此长的数据（例如内联文本 URL）。',
        'EntityMentionUserInvalidError': '你不能使用这个实体。',
        'MessageEmptyError': '发送了空或无效的 UTF-8 消息。',
        'MessageTooLongError': '消息太长。当前最大长度 为 4096 个 UTF-8 字符。',
        'MsgIdInvalidError': '对等体中使用的消息 ID 无效。',
        'PeerIdInvalidError': '使用了无效的 Peer 。确保传递正确的对等类型并且该值有效（例如，机器人无法 开始对话）。',
        'PollOptionInvalidError': '轮询选项使用了无效数据 （数据可能太长）。',
        'RandomIdDuplicateError': '您提供了一个已经使用过的随机 ID。',
        'ReplyMarkupInvalidError': '提供的回复标记无效。',
        'ReplyMarkupTooLongError': '嵌入在回复标 记按钮中的数据太多了。',
        'ScheduleBotNotAllowedError': '不允许机器人安排消息。',
        'ScheduleDateTooLateError': '您尝试安排的日期在未来太远（上次已知限制为 1 年零几个小时）。',
        'ScheduleStatusPrivateError': '如果他们的隐私未显示此信息，则您无 法在此人上线之前安排消息。',
        'ScheduleTooMuchError': '您无法在此聊天中安排更多消息（每个聊天的最后已知限制为 100）。',
        'TimeoutError': '获取数据时发生超时。',
        'UserIsBlockedError': '用户被阻止。',
        'UserIsBotError': '机器人无法向其他机器人发送消息。',
        'YouBlockedUserError': '你屏蔽了这个用户。',
        'BroadcastPublicVotersForbiddenError': '您不能在选民公开的情况下广播投票。',
        'ChatSendGifsForbiddenError': '您无法在此聊天中发送GIF。',
        'ChatSendMediaForbiddenError': '您无法在此聊天中发送媒体。',
        'ChatSendStickersForbiddenError': '您无法在此聊天中发送贴纸。',
        'GroupedMediaInvalidError': '无效的分组媒体。',
        'MediaEmptyError': '提供的媒体对象无效或当前帐户可能无法发送它（例如用户的游戏）。',
        'MessageIdsEmptyError': '未提供消息 ID。',
        'MessageIdInvalidError': '指定的消息ID无效或您无法对此类消息执行该操作。',
        'PtsChangeEmptyError': '没有 PTS 变化。',
        'RandomIdInvalidError': '提供的随机 ID 无效。',
        'InputConstructorInvalidError': '提供的构造函数无效。',
        'AboutTooLongError': '提供描述太长',
        'FirstNameInvalidError': 'First name 错误/异常'
    }
    for key in edict.keys():
        if key.lower() in err_type.lower():
            return edict[key]
    return err_type


# telethon 接口返回消息,替换为中文消息
def tg_cn_msg(msg):
    """替换为中文消息"""
    resp = {
        'msg': msg,
        'account_offline': False,
        'ban_account': False,
        'ban_target': False,
        'ban_proxy': False,
        'ban_user': False,
        'ban_content': False
    }
    try:
        mtype = msg_type(msg)
        if mtype:
            resp[mtype] = True
        resp['msg'] = msg2cn(msg)
        # if msg and type(msg) == str:
        #     msg = msg.lower()
        #     if "you can't send media in this chat" in msg:
        #         msg = msg2cn(msg)
        #         resp['ban_target'] = True
        #     elif "you can't write in this chat" in msg:
        #         msg = msg2cn(msg)
        #         resp['ban_target'] = True
        #     elif "The channel specified is private and you lack permission to access it. Another reason may be that you\
        #      were banned from it" in msg:
        #         msg = msg2cn(msg)
        #         resp['ban_account'] = True
        #     elif 'a wait of' in msg and 'seconds' in msg:
        #         """
        #        A wait of 496 seconds is required before sending another message in this chat (caused by ForwardMessagesRequest)
        #        """
        #         mc = re.search('\d+', msg)
        #         if mc:
        #             sec = mc.group()
        #             msg = '帐号被禁言%s秒' % (sec)
        #     elif 'was used under two different IP addresses simultaneously' in msg:
        #         msg = '禁止session帐号同时在不同IP下使用'
        #     elif 'The used phone number has been banned from Telegram' in msg:
        #         msg = msg2cn(msg)
        #         resp['account_offline'] = True
        #     elif 'deleted/deactivated/offline' in msg:
        #         msg = msg2cn(msg)
        #         resp['account_offline'] = True
        #     elif 'banned from sending messages in supergroups' in msg:
        #         msg = msg2cn(msg)
        #         resp['ban_account'] = True
        #     elif 'Connection to Telegram failed' in msg:
        #         msg = msg2cn(msg)
        #         resp['ban_proxy'] = True
        #     elif 'consecutive sign-in attempts failed. Aborting' in msg:
        #         msg = msg2cn(msg)
        #     elif 'The target user is not a member of the specified megagroup or channel' in msg:
        #         msg = msg2cn(msg)
        #     elif "The user's privacy settings do not allow you to do this " in msg:
        #         msg = msg2cn(msg)
        #     elif 'Too many requests' in msg:
        #         msg = msg2cn(msg)
        #         resp['ban_account'] = True
        #     elif 'No user has' in msg and 'as username' in msg:
        #         msg = msg2cn(msg)
        #         resp['ban_target'] = True
        #     elif 'Nobody is using this username, or the username is unacceptable' in msg:
        #         msg = msg2cn(msg)
        #         resp['ban_target'] = True
        #     elif 'cannot find any entity' in msg:
        #         msg = msg2cn(msg)
        #         resp['ban_target'] = True
        #     resp['msg'] = msg
    except Exception as e:
        err_log("tg_cn_msg:{}".format(str(e)))
    finally:
        return resp


# 获取socks, 将代理字符转换成sock代理格式, 支持username和password如:socks5://username:password@ip:port
def get_socks(proxy_str):
    _socks = None
    if '//' in proxy_str:
        mc = re.search(r'(.*)://(.*)', proxy_str)
        if mc:
            p_type = mc.group(1)
            if 'http' in p_type.lower():
                p_type = socks.HTTP
            elif 'socks4' in p_type.lower():
                p_type = socks.SOCKS4
            elif 'socks5' in p_type.lower():
                p_type = socks.SOCKS5
            p_str = mc.group(2)
            if p_str:
                if '@' in p_str:
                    _l = str.split(p_str, '@')
                    if _l:
                        user_pwd = _l[0]
                        u_p = str.split(user_pwd, ':')
                        username = u_p[0]
                        password = u_p[1]
                        ip_port = _l[1]
                        i_p = str.split(ip_port, ':')
                        ip = i_p[0]
                        port = int(i_p[1])
                        _socks = (p_type, ip, port, True, username, password)
                else:
                    i_p = str.split(p_str, ':')
                    ip = i_p[0]
                    port = int(i_p[1])
                    _socks = (p_type, ip, port)
    return _socks


# 根据session字符串, 固定随机硬件信息
def get_device_info_by_session_str(session_str, is_iphone=None):
    """根据session字符串, 固定随机硬件信息"""
    idict = {}
    android_model = [
        'HAWEI Mate30', 'HUAWEI P30', 'HUAWEI HONOR', 'HUAWEI Nova', 'Xiaomi',
        'OPPO Reno', 'VIVO IQOO', 'VIVO NEX', 'SAMSUNG NOTE', 'SAMSUNG S10',
        'OnePlus 7', 'OnePlus 8', 'Blackshark'
    ]
    iphone_model = [
        'iPhone 7', 'iPhone 7 Plus', 'iPhone 8', 'iPhone 8 Plus', 'iPhone 9',
        'iPhone 9 Plus', 'iPhone 10', 'iPhone 11', 'iPhone 12',
        'iPhone 12 Plus'
    ]
    model = random.choice(android_model)
    sign1 = ''.join(
        random.choice(string.digits + string.ascii_lowercase)
        for _ in range(4))
    sign2 = ''.join(
        random.choice(string.digits + string.ascii_lowercase)
        for _ in range(4))
    device_model = '{}-{}-{}'.format(model, sign1, sign2)
    system_version = str(random.randint(5, 10))
    a_version = '1.{}.{}'.format(random.randint(10, 30), random.randint(0, 9))
    if session_str:
        model_index = 9
        num_list = ['1', '5', '3', '7', '9', '6', '0', '4', '2', '8']
        num_list = re.findall(r'\d', session_str)
        if num_list:
            model_index = int(num_list[0])
        system_version = model_index
        model = android_model[model_index]
        sign1 = '{}{}{}'.format(num_list[0], num_list[1], num_list[2])
        sign2 = '{}{}{}'.format(num_list[-1], num_list[-2], num_list[-3])
        if is_iphone:
            model = iphone_model[model_index]
        device_model = '{}-{}-{}'.format(model, sign1, sign2)
        a_version = '1.{}.{}'.format(num_list[0], num_list[-1])

    # 手机品牌+型号 如:HUAWEI MATE30-sda1-3124
    default_device_model = str(device_model)
    # 平台系统版本号, 如:Adroid 10
    default_system_version = str(system_version)
    # 接口版本号, 如:1.18.2
    app_version = str(a_version)

    idict['default_device_model'] = default_device_model
    idict['default_system_version'] = default_system_version
    idict['app_version'] = app_version
    return idict


# 根据手机号或api_id生成手机硬件信息
def get_mobile_info(phone=None, api_id=False):
    """根据手机号或api_id生成手机硬件信息"""
    idict = {}
    android_model = [
        'HAWEI Mate30', 'HUAWEI P30', 'HUAWEI HONOR', 'HUAWEI Nova', 'Xiaomi',
        'OPPO Reno', 'VIVO IQOO', 'VIVO NEX', 'SAMSUNG NOTE', 'SAMSUNG S10',
        'OnePlus 7', 'OnePlus 8', 'Blackshark'
    ]
    iphone_model = [
        'iPhone 7', 'iPhone 7 Plus', 'iPhone 8', 'iPhone 8 Plus', 'iPhone 9',
        'iPhone 9 Plus', 'iPhone 10', 'iPhone 11', 'iPhone 12',
        'iPhone 12 Plus', 'iPhone XS'
    ]
    model = random.choice(android_model)
    sign1 = ''.join(
        random.choice(string.digits + string.ascii_lowercase)
        for _ in range(4))
    sign2 = ''.join(
        random.choice(string.digits + string.ascii_lowercase)
        for _ in range(4))
    device_model = '{}-{}-{}'.format(model, sign1, sign2)
    system_version = str(random.randint(5, 10))
    android_version_list = [
        '7.4.1', '7.4.0', '7.3.1', '7.3.0', '7.2.1', '7.2.0', '7.1.3', '7.1.2',
        '7.1.1', '7.1.0', '7.0.1', '7.0.0', '6.3.0', '6.2.0', '6.1.1'
    ]
    a_version = '1.{}.{}'.format(random.randint(10, 30), random.randint(0, 9))

    if phone:
        model_index = int(phone[-1])
        system_version = model_index
        # 平台系统版本号, 如:Adroid 10
        if str(system_version) == '0':
            system_version = '7'
        model = android_model[model_index]
        sign1 = phone[len(phone) - 3:len(phone)]
        sign2 = phone[-6:-3]
        device_model = '{}-{}-{}'.format(model, sign1, sign2)
        # a_version = '1.{}.{}'.format(phone[-4:-2], phone[-1])
        a_version = android_version_list[model_index]
        if api_id == '8':  # ios版本
            model = iphone_model[model_index]
            device_model = model
            ios_version_list = [
                '7.3.1', '7.3', '7.2.1', '7.2', '7.1.2', '7.1.1', '7.1',
                '7.0.2', '7.0.1', '7.0', '6.3.1', '6.3', '6.2.1', '6.2',
                '6.1.2', '6.1.1', '6.1', '6.0.1', '6.0'
            ]
            a_version = ios_version_list[model_index]
            ios_system_list = [
                '12.0', '12.1', '12.2', '12.3', '12.4', '11.0', '11.1', '11.2',
                '11.3', '11.4', '10.0', '10.1', '10.2', '10.3'
                '9.0', '9.1', '9.2', '9.3', '8.0', '8.1', '8.2', '8.3', '8.4',
                '7.0', '7.1', '7.2', '7.3', '7.4'
            ]
            system_version = ios_system_list[model_index]
        elif api_id == '2040':  # 桌面版
            device_model = 'PC 64bit'
            if model_index > 5:
                system_version = '10'
            else:
                system_version = '7'
            win_app_version_list = [
                '2.5.6', '2.5.5', '2.5.4', '2.5.3', '2.5.1', '2.5.0', '2.4.15',
                '2.4.14', '2.4.13', '2.4.12', '2.4.11', '2.4.10'
            ]
            a_version = win_app_version_list[model_index]

    # 手机品牌+型号 如:HUAWEI MATE30-sda1-3124
    default_device_model = str(device_model)
    default_system_version = str(system_version)
    # 接口版本号, 如:1.18.2
    app_version = str(a_version)

    idict['default_device_model'] = default_device_model
    idict['default_system_version'] = default_system_version
    idict['app_version'] = app_version
    return idict


# 将加密硬件信息字符串转成dict
def get_device_info_dict(st):
    """将加密硬件信息字符串转成dict"""
    j = {}
    if st:
        try:
            st = bytes(st, encoding='utf-8')
            a = DesDecrypt(st).decode()
            a = json.dumps(eval(a))
            j = json.loads(a)
        except:
            pass
    return j


# 获取本地ip地址
def get_my_ip(proxy=None):
    """
    查询本机ip地址
    :return: ip
    """
    try:
        my_ip = ''
        resp = requests.get('https://lumtest.com/myip.json')
        if resp and resp.status_code == 200:
            my_ip = resp.text
        if not my_ip:
            resp = requests.get('http://ip.42.pl/raw')
            if resp and resp.status_code == 200:
                my_ip = resp.text
        if not my_ip:
            resp = requests.get('http://jsonip.com')
            if resp and resp.status_code == 200:
                _json = json.loads(resp.text)
                # print(my_ip)
                my_ip = _json['ip']
        if not my_ip:
            resp = requests.get('http://httpbin.org/ip')
            if resp and resp.status_code == 200:
                _json = json.loads(resp.text)
                my_ip = _json['origin']
        if not my_ip:
            resp = requests.get('https://api.ipify.org/?format=json')
            if resp and resp.status_code == 200:
                _json = json.loads(resp.text)
                my_ip = _json['ip']
    finally:
        return my_ip



# 字符串中是否包含中文字符
def exist_cn_str(st):
    result = re.compile(u'[\u4e00-\u9fa5]')
    if result.search(st):
        return True
    else:
        return


# 下载文件
def download_file(url, file_path=None):
    if not file_path:
        _f = os.path.split(url)
        if _f:
            file_path = _f[1]
    if url and file_path:
        # 第一次请求是为了得到文件总大小
        r1 = requests.get(url, stream=True, verify=False)
        total_size = int(r1.headers['Content-Length'])

        # 这重要了，先看看本地文件下载了多少
        if os.path.exists(file_path):
            temp_size = os.path.getsize(file_path)  # 本地已经下载的文件大小
        else:
            temp_size = 0
        # # 显示一下下载了多少
        # print(temp_size)
        # print(total_size)
        if temp_size == total_size:
            # print('大小一致')
            return True
        else:
            # print('开始下载')
            # 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
            headers = {'Range': 'bytes=%d-' % temp_size}
            # 重新请求网址，加入新的请求头的
            r = requests.get(url, stream=True, verify=False, headers=headers)

            # 下面写入文件也要注意，看到"ab"了吗？
            # "ab"表示追加形式写入文件
            with open(file_path, "ab") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        temp_size += len(chunk)
                        f.write(chunk)
                        f.flush()

            #             ###这是下载实现进度显示####
            #             done = int(50 * temp_size / total_size)
            #             sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
            #             sys.stdout.flush()
            # print()  # 避免上面\r 回车符
            temp_size = os.path.getsize(file_path)  # 本地已经下载的文件大小
            if temp_size == total_size:
                # print('下载完成')
                return True


# 解压缩7zip文件
def unzip(file, delete=True):
    """解压文件 返回:目录地址"""
    try:
        shutil.register_archive_format('7zip',
                                       pack_7zarchive,
                                       description='7zip archive')
        shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
        if os.path.exists(file):
            d = './update'
            # print('开始解压文件,请稍等 ....')
            # 解压缩
            # archive=py7zr.SevenZipFile(file,mode='r')
            # archive.extract(path=d)
            # archive.close()
            shutil.unpack_archive(file, d)
            # print('文件解压完成.')
            if delete:
                os.remove(file)
            return d
    except Exception as e:
        err_log("文件解压缩失败:{}".format(str(e)))
        # print('文件解压异常')
        return


# 检查更新机制
def check_update():
    try:
        if os.path.exists('up.exe'):  # 存在更新程序
            if os.path.exists('update'):  # 存在更新包, 启动进行更新
                os.system('start "" "up.exe"')
                return False
            else:  # 没有更新目录, 则表示已经更新完成了. 删除up.exe即可.
                os.remove('up.exe')
    except:
        pass
    return True


# 超级加密
def dcode_en(st):
    key = "WXCZXF79"
    iv = 'WXLWM520'
    try:
        method = pyDes.des(key,
                           pyDes.CBC,
                           iv,
                           pad=None,
                           padmode=pyDes.PAD_PKCS5)
        k = method.encrypt(st)
        k = base64.b64encode(k)
        k = k.decode()
        # 栅栏加密
        zl = random.randint(2, int(len(k) / 2))
        scode = "{}{}".format(len(str(zl)), zl)
        k = zl_encode(k, zl)
        if len(k) > 7:
            k_list = list(k)
            k_list.insert(7, scode)
            k = ''.join(k_list)
        return k
    except Exception as e:
        # print('super_en',str(e))
        return


# 超级解密
def dcode_de(st):
    key = "WXCZXF79"
    iv = 'WXLWM520'
    try:
        if len(st) > 7:
            k_list = list(st)
            index = int(k_list[7])
            le = 8 + int(index)
            zl = ''.join(k_list[8:le])
            del k_list[7:le]
            st = ''.join(k_list)
            zl = int(zl)
            st = zl_decode(st, zl)
            if st:
                method = pyDes.des(key,
                                   pyDes.CBC,
                                   iv,
                                   pad=None,
                                   padmode=pyDes.PAD_PKCS5)
                k = base64.b64decode(st)
                k = method.decrypt(k)
                k = k.decode()
                return k
    except Exception as e:
        # print(str(e))
        return


def get_sign(len=17):
    """生成随机签名"""
    return str2Md5(RandomStr(len))  # http请求签名, 返回要核对,一致说明返回正确


def str2int(st):
    try:
        return int(st)
    except:
        return


def create_logger():
    logger = logging.getLogger("exception")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("exception.log")
    fmt = "\n[%(asctime)s-%(name)s-%(levelname)s]: %(message)s"
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def log_exception(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        logger = create_logger()
        try:
            fn(*args, **kwargs)
        except Exception as e:
            logger.exception("[Error in {}] msg: {}".format(__name__, str(e)))
            raise

    return wrapper


def list_sort(_d, lambda_func=lambda k: (k['a'], k['b']), reverse=False):
    """list中dict为元素的排序, 通过lambda获取的dict的key进行排序"""
    try:
        _d = sorted(_d, key=lambda_func,
                    reverse=reverse)  # 排序, 多个条件用,连接, reverse 正序/反序
        return _d
    except Exception as e:
        err_log('list_sort:{}'.format(str(e)))


def list_filter(_d, lambda_func=lambda x: (x['a'] != 24 and x['c'] != 32)):
    """list列表过滤, 根据lambda筛选dict中对应的key和value的对应条件"""
    try:
        _d = list(filter(lambda_func, _d))  # 列表过滤
        return _d
    except Exception as e:
        err_log('list_filter:{}'.format(str(e)))


def list_in_str(li, st, all=False):
    """判断list中的字符, 是否存在与指定字符串中[li: 列表, st:字符串, all: 列表中是否都存在与st中]"""
    status = False
    if li and st:
        for _l in li:
            if all:
                if _l in st:
                    status = True
                else:
                    status = False
            else:
                if _l in st:
                    status = True
                    break
    return status


def str_in_list(st, li):
    """字符串存在与list成员中"""
    for l in li:
        if st in l:
            return True
    return


def get_list_index(_list, key, value):
    """获取list中的index(成员为dict)"""
    try:
        if _list:
            for i in range(len(_list)):
                _l = _list[i]
                if _l[key] == value:
                    return i
    except Exception as e:
        err_log('get_list_index:{}'.format(str(e)))


# 压缩文件(将目录压缩成文件)
def compress_dir(dir, zp_file, password=None):
    try:
        with py7zr.SevenZipFile(zp_file, mode='w',
                                password=password) as archive:
            archive.writeall(dir)
            if os.path.exists(zp_file):
                return True
    except Exception as e:
        err_log(str(e))


# 解压缩文件
def decompress_file(file, path, password=None):
    try:
        with py7zr.SevenZipFile(file, mode='r', password=password) as z:
            if path:
                z.extractall(path=path)
            else:
                z.extractall()
        if os.path.exists(path):
            return True
    except Exception as e:
        err_log(str(e))


def path_win2linux(filepath):
    """路径windows格式转换成linux格式"""
    try:
        filepath = os.path.abspath(filepath)
        if '\\' in filepath:
            filepath = '/'.join(filepath.split(
                '\\'))  # transform the windows path to linux path
    finally:
        return filepath