# -*- coding:utf-8 -*-
import json
import os, sys, time, re, threading
import shutil
import mod.device as device, mod.app as app, mod.api as api
import uiautomator2 as u2
import phonenumbers, adbutils


if __name__ == '__main__':
    ld_path = r'D:\leidian\LDPlayer_en_4.0'
    index = 0
    ld = device.Ldmnq(ld_path, index)
    # resp = ld.adb_shell('getprop')
    # print(resp)
    ld.run_atx_agent()
    


    proxy = '192.168.0.106:10809'
    ld.unset_proxy()
    ld.set_proxy(proxy)

    # phone = '+84528399617'
    # tw = app.Twitter(ld)
    # tar = '/sdcard/Pictures/twitter/{}.tar.gz'.format(phone)
    
    # ld.kill_app(tw.package_name)
    # ld.backup_data(tw.package_name, tar)
    # ld.clear_app(tw.package_name)
    # ld.restore_data(tw.package_name, tar)



    # phone = "+14503297663"
    # phone_data = phonenumbers.parse(phone, None)
    # if phone_data:
    #     country_code = phone_data.country_code  # 电话国码
    #     national_number = phone_data.national_number  # 号码部分(无国码)


    # pkg = 'com.whatsapp'
    # ld.kill_app(pkg)
    # ld.clear_app(pkg)

    # device = ld.get_device_info()
    # print(json.dumps(device))


    # ld.set_device_info(phone)
    # device = ld.get_device_info()
    # print(json.dumps(device))



    # ws = app.WhatsApp(ld)

    # ws.reg_account(str(country_code), str(national_number))

    
    # tar = '/sdcard/Pictures/whatsapp/{}.tar.gz'.format(phone)
    # # ld.restore_data('com.whatsapp', tar)
    # ld.backup_data('com.whatsapp', tar)

    # # country = '1'
    # # phone = '2343800023'
    # # ws = app.WhatsApp(ld)
    
    # # ws.reg_account(country, phone)

