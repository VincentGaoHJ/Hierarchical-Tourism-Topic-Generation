# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/6/15
@Author: Haojun Gao
@Description: 
"""

import os
import shutil
import datetime
from visualize import visualize
from corpus_seed import corpus_seed
from corpus_split import corpus_split


def create_dir(data_path, dataset, rootNode):
    """
    为本次实验创建一个独立的文件夹
    把 data 文件夹中的初始文件拷贝到单独文件夹中
    :return:
    """
    root = os.getcwd()
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    folder = os.path.join(root, nowTime)
    # 创建文件夹
    os.makedirs(folder)

    shutil.copy(os.path.join(data_path, dataset, rootNode + ".csv"), folder)

    return folder


def read_temp(temp_file):
    nodes = {'*': [[], [], []]}
    file_node = []
    with open(temp_file, 'r') as f:
        for line in f:
            file_node.append(line[:-1])
    return file_node


def iteration(data_path, rootNode, used_word, dataset):
    temp_file = os.path.join(data_path, ".\\temp.txt")
    if not os.path.exists(temp_file):
        geo_noun, non_geo_noun, used_word, user_cut = corpus_seed(data_path, rootNode, used_word, rootNode, dataset)
        corpus_split(data_path, geo_noun, user_cut)
    else:
        file_node = read_temp(temp_file)
        f = open(temp_file, "r+")
        f.truncate()
        # print(file_node)
        for file in file_node:
            geo_noun, non_geo_noun, used_word, user_cut = corpus_seed(data_path, file, used_word, rootNode, dataset)
            corpus_split(data_path, geo_noun, user_cut)


def main(data_path, rootNode, dataset, dataset_id):
    MAX_LEVEL = 5

    folder = create_dir(data_path, dataset, rootNode)
    print(folder)

    # used_word = ["文章", "中国", "北京", '北京市', dataset_id]
    # used_word = ["文章", "中国", "云南", '昆明市', '昆明', dataset_id]
    # used_word = ["文章", "中国", "浙江省", "浙江", '杭州市', '杭州', dataset_id]
    # used_word = ["文章", "中国", "贵州省", "贵州", "贵阳", '贵阳市', dataset_id]
    used_word = ["文章", "自然语言处理", "NLP","机器", dataset_id]
    for level in range(MAX_LEVEL):
        print('\n================================== Running level ', level, ' ==================================\n')
        iteration(folder, rootNode, used_word, dataset)

    print(folder)
    visualize(folder, dataset_id)


if __name__ == '__main__':
    dataset = "zhihu"
    dataset_id = "nlp"

    data_path = ".\\data"
    rootNode = dataset_id + "_0"
    main(data_path, rootNode, dataset, dataset_id)
