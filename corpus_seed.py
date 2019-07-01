# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/6/30
@Author: Haojun Gao
@Description: 
"""

import os
import csv
import math
from collections import Counter
from geo_classify import get_classify


# 统计词频
def CountWord(comment_sentence):
    """

    :param POI: POI字符串
    :return:
    """
    comment = "/".join(comment_sentence)
    doc = comment.split('/')
    c = Counter(doc)
    cnt = []
    for k, v in c.items():
        cnt.append((k, v))
    cnt.sort(key=lambda x: x[1], reverse=True)
    return cnt


def generate_sentences(data_path, fileNode):
    file_name = fileNode.split("/")[-1]
    print(file_name)
    file_path = os.path.join(data_path, file_name + ".csv")
    user_cut = []
    with open(file_path) as t:
        reader = csv.reader(t)
        for sentence in reader:
            user_cut.append(sentence[0])
    return user_cut


def write_output(data_path, geo_noun, non_geo_noun, fileNode):
    temp_file = os.path.join(data_path, "temp.txt")
    with open(temp_file, 'a+', newline='') as file:
        writer = csv.writer(file)
        for sen in geo_noun:
            if fileNode == "0":
                writer.writerow(["*/{}".format(sen)])
            else:
                writer.writerow(["{}/{}".format(fileNode, sen)])

    result_file = os.path.join(data_path, "result.txt")
    with open(result_file, 'a+', newline='') as file:
        if fileNode == "0":
            file.write("*/top")
        else:
            file.write("\n" + str(fileNode))
        file.write('\t')
        num = len(non_geo_noun)
        for i in range(num):
            if i != 0:
                file.write(",")
            file.write(str(non_geo_noun[i]))


def judge_num(geo_left, count_cha, appear, item, prob, chongfu):
    if count_cha > 20:
        if (count_cha / appear) > 0.8:
            print("{} 为独立景点，单独出现比例 {} 够，可用于继续分割".format(item, prob))
            geo_left.append(item)
            print(geo_left)
        else:
            print("{} 不为独立景点，因为单独出现的比例 {} 不够，接下来判断其类型".format(item, prob))
            chongfu_count = Counter(chongfu)
            print(chongfu)
            print(chongfu_count)
    else:
        print("{} 不为独立景点，因为单独出现的总数 {} 不够".format(item, count_cha))

    return geo_left


def judge_entropy(geo_left, user_geo, item):
    for poi in geo_left:
        num_poi = 0
        num_item = 0
        both = 0
        for geo_comment in user_geo:
            if item in geo_comment:
                num_item += 1
            if poi in geo_comment:
                num_poi += 1
            if item in geo_comment and poi in geo_comment:
                both += 1
        total = len(user_geo)
        if both == 0:
            continue
        mutual_information = total * both / (num_poi * num_item)
        mutual_information = math.log2(mutual_information)
        print("{} 与 {} 的互信息量 {}".format(item, poi, mutual_information))
        if mutual_information >= 0:
            print("[结论] {} 不为独立景点，因为与 {} 互信息量大 {}".format(item, poi, mutual_information))
            return geo_left

    geo_left.append(item)

    return geo_left


def find_seed(user_cut, geo_noun):
    user_geo = []
    for sentence in user_cut:
        word_list = sentence.split('/')
        res = list(set(geo_noun).intersection(set(word_list)))
        if res:
            user_geo.append(res)
    print(user_geo)
    geo_left = []  # 用于保存留下的用于继续分裂的景点
    geo_conclude = []  # 用于保存当前判断的景点
    count_before = 0  # 不包含当前景点的计数
    count_after = 0  # 对包含当前景点的计数
    count_cha = 0  # 计算当前景点的差值
    for item in geo_noun:
        # print(geo_conclude)
        geo_conclude.append(item)
        # print(geo_conclude)
        i = 0
        appear = 0

        chongfu = []
        for single_geo in user_geo:
            res = list(set(geo_conclude).intersection(set(single_geo)))
            if res:
                i += 1
            if len(res) >= 2 and item in res:
                chongfu.extend(res)
            if item in single_geo:
                appear += 1

        count_after = i
        count_cha = count_after - count_before
        prob = count_cha / appear

        # geo_left = judge_num(geo_left, count_cha, appear, item, prob, chongfu)

        geo_left = judge_entropy(geo_left, user_geo, item)

        count_before = count_after

    print(geo_left)
    return geo_left


def corpus_seed(data_path, fileNode, used_word):
    print('\n==========================\n Running Node  ', fileNode, '\n==========================')

    user_cut = generate_sentences(data_path, fileNode)
    print("景点文章：", user_cut[:3])

    sort_Word = CountWord(user_cut)
    print("景点名词：", sort_Word[:10])

    geo_noun, non_geo_noun = get_classify(sort_Word, used_word)
    print("地理名词集合 {}".format(geo_noun))
    print("特征名词集合 {}".format(non_geo_noun))

    geo_noun = find_seed(user_cut, geo_noun)

    print("使用过的名词集合 {}".format(used_word))

    used_word.extend(geo_noun)
    used_word.extend(non_geo_noun)

    # 绘制绘图所用格式输出
    write_output(data_path, geo_noun, non_geo_noun, fileNode)

    return geo_noun, non_geo_noun, used_word, user_cut
