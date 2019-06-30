# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/6/15
@Author: Haojun Gao
@Description: 利用高德地图api实现地址和经纬度的转换
"""

import requests


def Gaode_respond(address, Key):
    parameters = {'address': address, 'key': Key}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer


if __name__ == '__main__':
    # 自己的Key
    # Gaode_Key = "32e3f5cd6d9a680627d031796f736387"
    # 网上的Key
    Gaode_Key = "cb649a25c1f81c1451adbeca73623251"

    address = '附近'
    answer = Gaode_respond(address, Gaode_Key)

    print(answer)
    print(address + "的经纬度：", answer['geocodes'][0]['location'])
