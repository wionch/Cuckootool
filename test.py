# -*- coding:utf-8 -*-
from typing import List
from phonenumbers import geodata
import uiautomator2 as u2, adbutils
import re, os, requests
import urllib.request
import json
import faker, phonenumbers
from phonenumbers import carrier, geocoder
from faker import Faker
from subprocess import Popen, PIPE
from coinpayments import CoinPaymentsAPI
import mod.func as func, mod.api as api

# if __name__ == '__main__':
#     # func.compress_dir('mod', 'nopwd.7z', password='wionch')
#     # func.decompress_file('nopwd.7z', None, password='wionch')
#     pass
#     a='12313'
#     print(a[0:-1])
def adb(adb_ip, command):
    """用nox_adb.exe执行adb命令, 包括push pull install等adb命令"""
    try:
        nox_adb_exe = 'adb/adb.exe'
        if adb_ip:
            adb_ip = '-s {}'.format(adb_ip)
        else:
            adb_ip = ''
        shell = '"{}" {} {}'.format(nox_adb_exe, adb_ip, command)
        print(shell)
        pop = Popen(shell, stdout=PIPE, shell=True)
        resp_list = pop.stdout.readlines()
        pop.stdout.close()
        resp_list = [x.decode('gbk').strip('\r\n') for x in resp_list]
        return resp_list
    except Exception as e:
        func.err_log(str(e))

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

if __name__ == '__main__':
    pass
    myip = func.get_my_ip()
    print(myip)
    # print(api.get_tx_info(txid='CPFI4SBSEUIRW83Y2NTDYTOKLF'))
    # print(get_location_by_cell(20465, 495, 3, 262))
    # print(get_location_by_cell(20442, 6015))
    # print(get_location_by_cell(1085, 24040))

    # ip = '172.22.74.113'
    # adb_ip = ip + ':5555'
    # # d = u2.connect(ip)
    # d = u2.connect_adb_wifi(adb_ip)
    # print(d.info)
    # # d.app_start('com.whatsapp')
    # d.open_url('https://www.baidu.com')
    # # output = d.shell('pm list packages').output
    # # print(output)
    # # print(type(output))

    # # aa = adbutils.AdbClient(host=ip, port=5555)
    # # print(aa.connect(adb_ip))
    # fake = Faker(locale ='zh_CN')
    # for _ in range(10):
    #     print(fake.name())
    #     print(fake.local_latlng())
    

    # phone = '+8613207475747'
    # p = phonenumbers.parse(phone, None)
    # n = p.national_number
    # print(n)
    # m = p.country_code

    # print(m)
    # print(p)
    # carr = carrier.name_for_number(p, 'en')
    # print(carr)
    # print(carrier.region_code_for_number(p))



    # print(geocoder.description_for_number(p, 'en'))
    # print(geocoder.country_mobile_token(p.country_code))
    # print(geocoder.country_name_for_number(p, 'en'))
    # print(geocoder.description_for_valid_number(p, 'en'))
    # print(geocoder.national_significant_number(p))
    # print(geocoder.number_type(p))
    # print(geocoder.region_code_for_country_code(p.country_code))
    # print(geocoder.region_code_for_number(p))
    # print(geocoder.region_codes_for_country_code(p.country_code))

    # file = 'mcc.txt'
    # if os.path.exists(file):
    #     content = func.ReadTxt(file)
    #     if content and type(content)==list:
    #         content = json.loads(content[0])
    #         print(type(content))
    #         print(len(content))
    #         for c in content:
    #             print(c)