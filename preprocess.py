# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/6/14
@Author: Haojun Gao
@Description:
"""

import os
import re
import csv
from BaiduApi_fenci import get_baidu_nlp_token, Baidu_fenci_respond


# 准备工作
def init():
    """
    设置结果数据要保存的文件夹
    :return:
    """
    data_path = ".\\data"
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    return data_path


def readfile():
    """
    加载 comment_all, 提取 commentary_user, comment_id
    :return:
    """
    comment_sentence = []
    with open('.\\raw_data\\comment_all.csv', 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            comment = line[2]
            comment_list = re.split("。|\n", comment)  # 按句子划分
            comment_list = [i for i in comment_list if i != ""]  # 删除空值
            for sentence in comment_list:
                comment_sentence.append(sentence)

            # 作为文章与文章之间的分隔符
            comment_sentence.append("文章")

    # 加载停用词
    with open('.\\raw_data\\stop_words.txt') as f1:
        stopwords = f1.read().split()

    return comment_sentence, stopwords


def is_uchar(term):
    """
    每个词组中，只要含有中文字符就保留
    :param term: 字符串
    :return:
    """

    for i in range(len(term)):
        if not (u'\u4e00' <= term[i] <= u'\u9fa5'):
            return False
    return True


def part_of_speech(user_cut, Flag, stopwords):
    """
    判断词性，并进行筛选，同时构建词表（地理名词，特征名词（非地理名词））
    :param user_cut: 列表，元素是评论字符串
    :param Flag:
    :return:
        POIi_new:
    """

    # 准备百度接口认证
    token = get_baidu_nlp_token()

    geo = set()
    non_geo = set()

    num = len(user_cut)
    batch_string = ""
    user_last = []
    i = 0
    for single in user_cut:
        if i == 10000:
            pass
        i += 1
        batch_string = '分割'.join([batch_string, single])
        if len(batch_string) >= 10000:
            print("[仅仅留下名词，构建地理与非地理名词词表] {}/{}".format(i, num))

            try:
                data_fenci = Baidu_fenci_respond(batch_string, token)
            except Exception:
                print("本次请求失败，这一次的和下一次的一起申请")
                continue

            if not data_fenci.__contains__("items"):
                batch_string = ""
                continue

            seg_save = []
            for item in data_fenci["items"]:
                ci = item["item"]
                if len(ci) <= 1 or ci in stopwords or is_uchar(ci) is False:
                    continue
                if ci == "文章":
                    user_last.append("文章")
                    continue
                elif item["pos"] in Flag:
                    seg_save.append(ci)
                    non_geo.add(ci)
                elif item["ne"] in Flag:
                    seg_save.append(ci)
                    geo.add(ci)
                elif ci == "分割":
                    if seg_save:
                        comment = '/'.join(seg_save)
                        user_last.append(comment)
                        seg_save = []

            batch_string = ""

    return user_last, geo, non_geo


if __name__ == '__main__':
    # 设置结果数据保存文件夹
    data_path = init()

    # 读取初始文件以及停用词词表
    comment_sentence, stopwords = readfile()
    print(comment_sentence[:1])

    # 按照词性进行筛选，并且构建词表
    Flag = ['an', 'g', 'n', 'nr', 'ns', 'nt', 'nz', 'LOC', 'ORG']
    user_last, geo, non_geo = part_of_speech(comment_sentence, Flag, stopwords)

    # 保存地理名词文件
    with open('geo_noun.txt', 'w') as f:
        for item in geo:
            f.write(item + "\n")

    # 保存特征名词（非地理名词）文件
    with open('non_geo_noun.txt', 'w') as f:
        for item in non_geo:
            f.write(item + "\n")

    # 保存删除无用信息的评论文件
    result_path = os.path.join(data_path, "0.csv")
    with open(result_path, 'w', newline='') as t:
        writer = csv.writer(t)
        for sentence in user_last:
            writer.writerow([sentence])
