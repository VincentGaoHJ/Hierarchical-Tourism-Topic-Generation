# -*- coding: utf-8 -*-
"""
@Date: Created on Tue Dec 11 13:40:14 2018
@Author: Haojun Gao
@Description: 
"""

import os
import urllib3
from BaiduApi import Baidu_respond
from GaodeApi import Gaode_respond
from TencentApi import Tencent_respond

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_key():
    # 高浩峻
    # AK = "t6Ziitq1IK5kRPTI5pAKimSHbf42SnDw"
    # SK = "Q5grL5nGVlSxzHHRmTannmunSL6v17F1"
    # 黄谨楠
    # AK = "fXUrG1FWcynpIxliBinP1ur2bYli1rLy"
    # SK = "gs00n1eRdKdl3MywoaCfBRrZpZQLFcK4"
    # 孙威
    Baidu_AK = "Wq2UQsQTQ7Izmd4ZoDxjUvAcRwP9ajPb"
    Baidu_SK = "txDeX1YhBkFrNvNPdjxfTsDbSKcrTpPo"

    # 自己的Key
    # Gaode_Key = "32e3f5cd6d9a680627d031796f736387"
    # 网上的Key
    Gaode_Key = "cb649a25c1f81c1451adbeca73623251"

    Tencent_key = "AA5BZ-SBDCI-MF2G4-5Z65Z-5EU2Q-KOBHH"  # Tencent 开发者密钥ID

    return Baidu_AK, Baidu_SK, Gaode_Key, Tencent_key


def geo_verify(noun):
    Baidu_AK, Baidu_SK, Gaode_Key, Tencent_key = get_key()
    # 百度API验证
    # print("百度API验证")
    data_json = Baidu_respond(noun, Baidu_AK, Baidu_SK)
    if data_json["status"] != 0:
        print("{} 百度验证失败，归为特征词".format(noun))
        return False

    # 高德API验证
    # print("高德API验证")
    answer = Gaode_respond(noun, Gaode_Key)
    if not answer:
        print("{} 高德验证失败，归为特征词".format(noun))
        return False

    # 腾讯API验证
    # print("腾讯API验证")
    category = Tencent_respond(noun, Tencent_key)
    if "旅游景点" not in category and "文化场馆" not in category:
        print("{} 腾讯验证失败，归为特征词".format(noun))
        return False

    print("{} 验证成功，归为地理名词".format(noun))
    return True


def get_set_geo(dataset, dataset_id):
    set_geo = set()
    file_path = os.path.join("data/", dataset, dataset_id + "_geo_noun.txt")
    with open(file_path, 'r') as file_to_read:
        item = file_to_read.readline()
        while item:
            set_geo.add(item[:-1])
            item = file_to_read.readline()
    return set_geo


def get_classify(user_cut, used_word, dataset, dataset_id):
    set_geo = get_set_geo(dataset, dataset_id)
    geo_noun = []
    non_geo_noun = []
    for item in user_cut:
        if item[0] in used_word:
            continue
        # if geo_verify(item[0]):
        if item[0] in set_geo:
            geo_noun.append(item[0])
        else:
            non_geo_noun.append(item[0])

    return geo_noun[:20], non_geo_noun[:20]


if __name__ == '__main__':
    user_cut = [('北京', 27563), ('地方', 15142), ('感觉', 9820), ('味道', 9368), ('建筑', 6638), ('东西', 5274), ('故宫', 5234),
                ('中国', 5171), ('特色', 5025), ('长城', 4949), ('时间', 4694), ('胡同', 4626), ('附近', 3337), ('烤鸭', 3227),
                ('朋友', 3174), ('风景', 3025), ('小时', 3015), ('景色', 3005), ('口味', 2702), ('博物馆', 2459), ('天安门', 2417),
                ('颐和园', 2280), ('文化', 2121), ('王府井', 2032), ('西单', 2022), ('交通', 1987), ('旁边', 1973), ('皇帝', 1944),
                ('北京市', 1875), ('世界', 1868)]
    used_word = []

    geo_noun, non_geo_noun = get_classify(user_cut, used_word, province_id)

    print("地理名词集合 {}".format(geo_noun))
    print("特征名词集合 {}".format(non_geo_noun))
