# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/6/14
@Author: Haojun Gao
@Description:
"""

import os
import re
import csv
import threading
from proxy_github import getProxy
from BaiduApi_fenci import get_baidu_nlp_token, Baidu_fenci_respond


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


# 准备工作
def init(dataset):
    """
    设置结果数据要保存的文件夹
    :return:
    """
    data_path = "./data"
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    data_path = os.path.join(data_path, dataset)
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    return data_path


def multi_threading(batch_string_list, token_pool, ip_list):
    threads = []
    thread_num = len(token_pool) * 2
    print("[构造多线程] 一共能构造 {} 个线程".format(thread_num))
    nloops = range(thread_num)

    for i in nloops:
        token_num = i % 7
        print("[构造多线程] 正在使用第 {} 个 token".format(token_num))
        t = MyThread(Baidu_fenci_respond, (batch_string_list[i], token_pool[token_num], ip_list[token_num]), Baidu_fenci_respond.__name__)
        threads.append(t)

    for i in nloops:  # start threads 此处并不会执行线程，而是将任务分发到每个线程，同步线程。等同步完成后再开始执行start方法
        print("[启动多线程] 正在启动第 {} 个 线程".format(i))
        threads[i].start()

    for i in nloops:  # jion()方法等待线程完成
        threads[i].join()
        print("[运行多线程] 第 {} 个 线程已结束".format(i))

    return threads


def readfile(dataset_id, dataset):
    """
    加载 comment_all, 提取 commentary_user, comment_id
    :return:
    """
    comment_sentence = []
    stopwords = []
    if dataset == "mafengwo":
        with open('./raw_data/mafengwo/' + dataset_id + '_comment_all.csv', 'r', encoding='utf-8-sig') as csvfile:
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
        with open('./raw_data/mafengwo/stop_words.txt', encoding='utf-8-sig') as f1:
            stopwords = f1.read().split()

    elif dataset == "zhihu":
        with open('./raw_data/zhihu/' + dataset_id + '_answers.csv', 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                # question = line[2]
                comment = line[3]
                comment_list = re.split("。|\n", comment)  # 按句子划分
                comment_list = [i for i in comment_list if i != ""]  # 删除空值
                for sentence in comment_list:
                    comment_sentence.append(sentence)

                # 作为文章与文章之间的分隔符
                comment_sentence.append("文章")

        # 加载停用词
        with open('./raw_data/zhihu/stop_words.txt', encoding='utf-8-sig') as f1:
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


def single_thread(user_cut, token_pool, Flag, Flag_geo):
    geo = set()
    non_geo = set()
    num = len(user_cut)
    batch_string = ""
    user_last = []
    i = 0
    for single in user_cut:
        i += 1
        batch_string = '分割'.join([batch_string, single])
        if len(batch_string) >= 10000:
            print("[仅仅留下名词，构建地理与非地理名词词表] {}/{}".format(i, num))

            try:
                # print(batch_string)
                data_fenci = Baidu_fenci_respond(batch_string, token_pool[0])
                # print(data_fenci)
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
                elif item["ne"] in Flag_geo or item["pos"] in Flag_geo:
                    seg_save.append(ci)
                    geo.add(ci)
                elif ci == "分割":
                    if seg_save:
                        comment = '/'.join(seg_save)
                        user_last.append(comment)
                        seg_save = []

            batch_string = ""
            # break

    return user_last, geo, non_geo


def multi_thread(user_cut, token_pool, Flag, Flag_geo):
    thread_num = len(token_pool) * 2
    geo = set()
    non_geo = set()
    num = len(user_cut)
    batch_string = ""
    user_last = []
    batch_string_list = []
    i = 0
    ip_list = getProxy(7)
    for single in user_cut:
        i += 1
        batch_string_after = '分割'.join([batch_string, single])
        if len(batch_string_after) <= 10000:
            batch_string = batch_string_after
        else:
            batch_string_list.append(batch_string)
            batch_string = single
            if len(batch_string_list) == thread_num:
                print("[仅仅留下名词，构建地理与非地理名词词表] {}/{}".format(i, num))
                try:
                    threads = multi_threading(batch_string_list, token_pool, ip_list)
                except Exception:
                    print("本次请求失败")
                    # break
                    continue

                k = 0
                for thread in threads:
                    k += 1
                    data_fenci = thread.get_result()
                    # print(data_fenci)

                    if data_fenci is None:
                        print("[解析词表] 第 {} 个线程抓取失败".format(k))
                        ip_list = getProxy(7)
                        continue

                    if not data_fenci.__contains__("items"):
                        print(data_fenci)
                        print("[解析词表] 第 {} 个线程抓取无结果".format(k))
                        ip_list = getProxy(7)
                        continue

                    # print(data_fenci["text"])
                    print("[解析词表] 正在解析第 {} 个线程抓取的结果".format(k))


                    seg_save = []
                    for item in data_fenci["items"]:
                        ci = item["item"]
                        # if len(ci) <= 1 or ci in stopwords or is_uchar(ci) is False:
                        if len(ci) <= 1 or ci in stopwords:
                            continue
                        if ci == "文章":
                            user_last.append("文章")
                            continue
                        elif item["pos"] in Flag:
                            seg_save.append(ci)
                            non_geo.add(ci)
                        elif item["ne"] in Flag_geo or item["pos"] in Flag_geo:
                            seg_save.append(ci)
                            geo.add(ci)
                        elif ci == "分割":
                            if seg_save:
                                comment = '/'.join(seg_save)
                                user_last.append(comment)
                                seg_save = []
                batch_string_list = []
                # break

    return user_last, geo, non_geo


def part_of_speech(user_cut, stopwords, dataset):
    """
    判断词性，并进行筛选，同时构建词表（地理名词，特征名词（非地理名词））
    :param user_cut: 列表，元素是评论字符串
    :param Flag:
    :return:
        POIi_new:
    """

    Flag = []
    Flag_geo = []
    if dataset == "mafengwo":
        Flag = ['an', 'g', 'n', 'nr', 'ns', 'nt', 'nz']
        Flag_geo = ['LOC', 'ORG']

    elif dataset == "zhihu":
        Flag = ['an', 'g', 'n']
        Flag_geo = ['nr', 'ns', 'nt', 'nz', 'nw', 'LOC', 'ORG']

    # 准备百度接口认证
    token_pool = get_baidu_nlp_token()

    # user_last, geo, non_geo = single_thread(user_cut, token_pool, Flag, Flag_geo)
    user_last, geo, non_geo = multi_thread(user_cut, token_pool, Flag, Flag_geo)

    return user_last, geo, non_geo


if __name__ == '__main__':

    dataset = "zhihu"
    dataset_id = "nlp"

    # 设置结果数据保存文件夹
    data_path = init(dataset)

    # 读取初始文件以及停用词词表
    comment_sentence, stopwords = readfile(dataset_id, dataset)
    print(comment_sentence[:1])

    # 按照词性进行筛选，并且构建词表
    user_last, geo, non_geo = part_of_speech(comment_sentence, stopwords, dataset)

    # 保存地理名词文件
    geo_path = os.path.join(data_path, dataset_id + '_geo_noun.txt')
    with open(geo_path, 'w') as f:
        for item in geo:
            f.write(item + "\n")

    # 保存特征名词（非地理名词）文件
    nongeo_path = os.path.join(data_path, dataset_id + '_non_geo_noun.txt')
    with open(nongeo_path, 'w') as f:
        for item in non_geo:
            f.write(item + "\n")

    # 保存删除无用信息的评论文件
    result_path = os.path.join(data_path, dataset_id + "_0.csv")
    with open(result_path, 'w', newline='') as t:
        writer = csv.writer(t)
        for sentence in user_last:
            writer.writerow([sentence])
