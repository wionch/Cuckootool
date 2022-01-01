# -*- coding:utf-8 -*-
import uiautomator2 as u2
import mnq.app as app


class UI2(object):
    def __init__(self,ip):
        self.ip=ip
        self.tg=app.Telegram()
    def run(self):
        d=u2.connect(self.ip)
        xp=self.tg.ui_dict('首页','connecting')
        print(d.xpath(xp).wait(10))
        print(d.info)
    # xpath是否存在
    # xpath等待
    # 点击xpath
    def click_xpath(self,index,key):
        pass
    # 设置代理
    