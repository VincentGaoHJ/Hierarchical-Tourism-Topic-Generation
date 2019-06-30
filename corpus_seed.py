# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/6/30
@Author: Haojun Gao
@Description: 
"""

import os
import csv
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


def corpus_seed(data_path, fileNode, used_word):
    print('\n==========================\n Running Node  ', fileNode, '\n==========================')
    file_name = fileNode.split("/")[-1]
    print(file_name)
    file_path = os.path.join(data_path, file_name + ".csv")
    user_cut = []
    with open(file_path) as t:
        reader = csv.reader(t)
        for sentence in reader:
            user_cut.append(sentence[0])

    print("景点文章：", user_cut[:3])

    sort_Word = CountWord(user_cut)
    print("景点名词：", sort_Word[:10])

    geo_noun, non_geo_noun, used_word = get_classify(sort_Word, used_word)

    print("地理名词集合 {}".format(geo_noun))
    print("特征名词集合 {}".format(non_geo_noun))

    temp_file = os.path.join(data_path, "temp.txt")

    # 绘制绘图所用格式输出
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

    return geo_noun, non_geo_noun, used_word, user_cut
