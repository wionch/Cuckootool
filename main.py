# -*- coding:utf-8 -*-

import os
# os.system("mitmdump --mode upstream:http://127.0.0.1:10809")

from mitmproxy import http
import typing

# This scripts demonstrates how mitmproxy can switch to a second/different upstream proxy
# in upstream proxy mode.
#
# Usage: mitmdump -U http://default-upstream-proxy.local:8080/ -s change_upstream_proxy.py
#
# If you want to change the target server, you should modify flow.request.host and flow.request.port


"""
# 先确定有正常默认的upstream代理, 请求需要先过默认代理, 再通过py进行代理修改
# 可以先用mit程序 mit.exe -p 8089 启动一个默认代理(注意: 无法访问墙外), 再启动一个mitmdump代理.
# 或者可以从代理ip列表中指认一个默认代理, 再通过py进行代理修改
mitmdump --mode upstream:http://127.0.0.1:8089 -s E:\Python\Mimtproxy\main.py --ssl-insecure  # 有效
"""

def proxy_address(flow: http.HTTPFlow) -> typing.Tuple[str, int]:
    # Poor man's loadbalancing: route every second domain through the alternative proxy.
    # if hash(flow.request.host) % 2 == 1:
    #     proxy = ("127.0.0.1", 10809)
    # else:
    #     proxy = ("127.0.0.1", 10809)

    if 'ip138.com' in flow.request.host:
        proxy = ("127.0.0.1", 10809)
    elif flow.request.host in ['httpbin.org', 'youtube.com']:
        proxy = ('127.0.0.1', 10809)
    else:
        proxy = None

    return proxy

def request(flow: http.HTTPFlow) -> None:
    if flow.request.method == "CONNECT":
        # If the decision is done by domain, one could also modify the server address here.
        # We do it after CONNECT here to have the request data available as well.
        return
    address = proxy_address(flow)
    print('address', address)
    if flow.live and address:
        print('url', flow.request.url)
        flow.live.change_upstream_proxy_server(address)  # type: ignore