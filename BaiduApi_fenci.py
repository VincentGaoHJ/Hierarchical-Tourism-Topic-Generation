# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/6/29
@Author: Haojun Gao
@Description: 
"""

# -*- coding: utf-8 -*-

import requests
import json


def get_baidu_nlp_token():
    """
    根据百度的接口，生成token
    :param client_id: AK
    :param client_secret: SK
    :return: access_token
    """

    # 高浩峻
    # client_id = "RBaTvGPi3xOTv1MRTgzRMVbD"
    # client_secret = "5qeUSdMBDIG70WLQTh7IeIdkeGrEbxQ9"

    # 黄晔熙
    # client_id = "5zV1XUeR5oGVKvF6si1Oesdi"
    # client_secret = "mhauYZnURRDVCjdsZ1R3H0xd2COsE83k"

    # 刘芷奇
    client_id = "kIZWUDcTaMwIV1yfZLsXuDXm"
    client_secret = "ogBKBp5I92s1sTw8rkPsK7YTCgXj47gq"

    # get token url
    access_token_url = "https://aip.baidubce.com/oauth/2.0/token"

    # hard code
    grant_type = "client_credentials"

    payload = {'grant_type': grant_type, 'client_id': client_id, 'client_secret': client_secret}
    rsp = requests.get(access_token_url, payload)
    rspdata = json.loads(json.dumps(rsp.json()))
    access_token = rspdata['access_token']

    return access_token


def Baidu_fenci_respond(data, access_token):
    """
    向用户提供分词、词性标注、专名识别三大功能；能够识别出文本串中的基本词汇（分词）
    对这些词汇进行重组、标注组合后词汇的词性，并进一步识别出命名实体。
    :param data: 文本串
    :param access_token: 百度认证
    :return: rspdata
    """
    # 词法分析
    header = {'Content-Type': 'application/json'}
    body = {'text': data}
    post_url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer" + "?access_token=" + access_token
    rsp = requests.post(post_url, headers=header, data=json.dumps(body))
    rspdata = json.loads(json.dumps(rsp.json()))

    return rspdata


def Baidu_entity_respond(data, access_token):
    """
    实体标注接口，支持输入一段中文短文本（64 个汉字），识别短文本中的实体，并给出实体的分类、描述及百科实体链接等 5000 次 / 天
    :param data: 中文短文本
    :param access_token: 百度认证
    :return: rspdata
    """
    header = {'content-type': 'application/json'}
    body = {'data': data}
    post_url = "https://aip.baidubce.com/rpc/2.0/kg/v1/cognitive/entity_annotation" + "?access_token=" + access_token
    print(post_url)
    rsp = requests.post(post_url, headers=header, data=json.dumps(body))
    rspdata = json.loads(json.dumps(rsp.json()))
    return rspdata


if __name__ == '__main__':

    test_data = "今天中午去参观了首都体育馆，北京大学，八达岭长城还有故宫博物院与紫禁城,地方，风景与好看"
    print(test_data)

    token = get_baidu_nlp_token()

    data_fenci = Baidu_fenci_respond(test_data, token)

    for item in data_fenci["items"]:
        if item["pos"] != "":
            print(item["pos"], end=" ")
        else:
            print(item["ne"], end=" ")
        print(item["item"], end=" ")
        print(item["basic_words"], end="\n")

    data_entity = Baidu_entity_respond(test_data, token)

    for item in data_entity["entity_annotation"]:
        print(item["mention"], end=" ")
        print(item["desc"], end=" ")
        print(item["concept"], end="\n")
