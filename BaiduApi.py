# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/6/15
@Author: Haojun Gao
@Description: 
"""

# !/usr/bin/python
# coding:utf-8


import hashlib
import requests
from urllib import parse


def get_url(address, AK, SK):
    # 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=你的ak
    # queryStr = '/geocoder/v2/?address=%s&output=json&ak=' % address
    queryStr = "/geocoder/v2/?address={}&output=json&ak={}".format(address, AK)

    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")

    # 在最后直接追加上yoursk
    rawStr = encodedStr + SK

    # 计算sn
    sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())

    # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")

    return url


def Baidu_respond(poi, AK, SK):
    url = get_url(poi, AK, SK)

    response = requests.get(url)

    return response.json()


if __name__ == '__main__':
    # 高浩峻
    Baidu_AK = "t6Ziitq1IK5kRPTI5pAKimSHbf42SnDw"
    Baidu_SK = "Q5grL5nGVlSxzHHRmTannmunSL6v17F1"

    # 黄谨楠
    # Baidu_AK = "fXUrG1FWcynpIxliBinP1ur2bYli1rLy"
    # Baidu_SK = "gs00n1eRdKdl3MywoaCfBRrZpZQLFcK4"

    # 孙威
    # Baidu_AK = "Wq2UQsQTQ7Izmd4ZoDxjUvAcRwP9ajPb"
    # Baidu_SK = "txDeX1YhBkFrNvNPdjxfTsDbSKcrTpPo"

    poi = "旁边"

    data_json = Baidu_respond(poi, Baidu_AK, Baidu_SK)
    if data_json["status"] == 0:
        print("{} 是地理名字，保留".format(poi))
    elif data_json["status"] == 1 or data_json["status"] == 2:
        print(data_json["msg"])
    elif data_json["status"] == 302:
        print(data_json["message"])
    else:
        print(data_json)
