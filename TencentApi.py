# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/6/15
@Author: Haojun Gao
@Description: 
"""

import requests
import pandas as pd
from collections import Counter


# 城市内搜索结果
def Tencent_respond(address, key):
    df = pd.DataFrame(columns=('ID', '店名', '地址', '电话', '类别', '纬度', '经度', '邮编', '省', '市', '区'))
    x = 0

    page = 1
    class_category = []
    url_base = "https://apis.map.qq.com/ws/place/v1/search?"
    url_para = 'boundary=region({},0)&page_size=20&page_index={}&keyword={}&orderby=_distance&key={}'.format(
                "北京", page, address, key)
    url = url_base + url_para

    req = requests.get(url=url, verify=False).json()
    data = req['data']
    if data != []:
        for j in data:
            # 构造大类别
            class_category.append(j['category'].split(":")[0])

            # id = j['id']  # ID
            # title = j['title']  # 店名
            # addr = j['address']  # 地址
            # tel = j['tel']  # 电话
            # category = j['category']  # 类别
            # lat = j['location']['lat']  # 纬度
            # lng = j['location']['lng']  # 经度
            # adcode = j['ad_info']['adcode']  # 邮编
            # province = j['ad_info']['province']  # 省
            # city = j['ad_info']['city']  # 市
            # district = j['ad_info']['district']  # 区
            #
            # print(id, title, addr, tel, category, lat, lng, adcode, province, city, district)
            # df.loc[x] = [id, title, addr, tel, category, lat, lng, adcode, province, city, district]
            # x = x + 1

    # 对大类别进行排序
    c = Counter(class_category)
    cnt = []
    for k, v in c.items():
        cnt.append((k, v))
    cnt.sort(key=lambda x: x[1], reverse=True)

    # 留下大类别中的前三个作为这个名词的类别
    class_belong = []
    for item in cnt:
        class_belong.append(item[0])

    return class_belong


if __name__ == '__main__':
    Tencent_key = "AA5BZ-SBDCI-MF2G4-5Z65Z-5EU2Q-KOBHH"  # 开发者密钥ID
    address = "附近"
    category = Tencent_respond(address, Tencent_key)
    print(category)
