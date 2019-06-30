# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/6/14
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


def corpus_split(data_path, fileNode, used_word):
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

    article = []
    for sentence in user_cut:
        # 如果没有遇到文章分割符，那么这一句话就归到一篇文章中
        if not sentence == "文章":
            article.append(sentence)
        # 遇到文章分隔符后，对文章中的句子进行势力划分，写入势力划分文档，将文章清零，将势力范围清空，将势力景点置零
        else:
            influPoi = ""
            influZone = []
            for article_elem in article:
                word_list = article_elem.split('/')
                # 判断句子中有没有分割词
                res = list(set(geo_noun).intersection(set(word_list)))
                if len(res) == 0:
                    # print("无分割词，放入势力范围区：{}".format(sentence))
                    influZone.append(article_elem)
                else:
                    # 如果之前没有出现过景点，那么缓冲区中的句子归这句最早出现的景点
                    if influPoi == "":
                        influPoi = res[0]
                        # print("无分割词，势力范围归此句分割词：{}（出现多个分割词归最早出现的分割词）".format(influPoi))

                    # 将缓冲区内的句子划归为上句话最后出现的景点
                    # print("势力范围共 {} 个句子归分割词：{}".format(len(influZone), influPoi))
                    save_path = os.path.join(data_path, str(influPoi) + ".csv")
                    with open(save_path, 'a+', newline='') as file:
                        writer = csv.writer(file)
                        for sen in influZone:
                            writer.writerow([sen])
                        writer.writerow(["文章"])

                    # 将这句话划归为所有出现了的景点
                    for poi in res:
                        save_path = os.path.join(data_path, str(poi) + ".csv")
                        with open(save_path, 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([article_elem])
                            writer.writerow(["文章"])

                    # 设置下一次缓冲区的归属景点，以及将缓冲区清零
                    influPoi = res[-1]
                    influZone = []

            # 循环完了之后，如果最后几句话存在，且前面有景点出现过，那么这几句话归前面的景点
            if influPoi != "" and influZone != []:
                save_path = os.path.join(data_path, str(influPoi) + ".csv")
                with open(save_path, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    for sen in influZone:
                        writer.writerow([sen])
                    writer.writerow(["文章"])

            # 清空文章内容
            article = []


if __name__ == '__main__':
    dirs = ""
    data_path = os.path.join(dirs, "data")
    result_path = os.path.join(data_path, "result.csv")
    used_word = ["中国", "时间", '风景', '景色']
    corpus_split(data_path, "0", used_word)
