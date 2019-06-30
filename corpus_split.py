# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/6/14
@Author: Haojun Gao
@Description: 
"""

import os
import csv


def corpus_split(data_path, geo_noun, user_cut):
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
