# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/8/5
@Author: Haojun Gao
@Description: 
"""

import os
import requests
from bs4 import BeautifulSoup


def get_set_geo(dataset, dataset_id):
    set_geo = set()
    file_path = os.path.join("data/", dataset, dataset_id + "_geo_noun.txt")
    with open(file_path, 'r') as file_to_read:
        item = file_to_read.readline()
        while item:
            set_geo.add(item[:-1])
            item = file_to_read.readline()
    return set_geo


def get_synonym(text):
    synonym_list = []
    res1 = text.find_all(id="synonyms")
    if len(res1) == 0:
        return synonym_list
    synonym = res1[0].get_text()
    synonym_list = synonym.split("\n")
    synonym_list = [i for i in synonym_list if i != '']
    return synonym_list


def entity_recognition(text):
    res1 = text.find_all("title")
    if len(res1) == 0:
        return False
    if "Error" in str(res1[0]):
        return False
    return True


def bigcilin_respond(Key):
    parameters = {'q': Key}
    base = 'http://www.bigcilin.com/WSDTest/'
    try:
        response = requests.get(base, parameters, timeout=5)
        text = response.text
    except:
        text = ""

    answer = BeautifulSoup(text, "lxml")

    return answer


if __name__ == '__main__':

    dataset = "mafengwo"
    dataset_id = "Beijing"
    data_path = ".\\data"

    set_geo = get_set_geo(dataset, dataset_id)

    print(set_geo)

    used_geo = set()

    synonym_list = []

    for item in set_geo:
        if item in used_geo:
            print("[entity recognition] {} is a synonym of an entity.".format(item))
        key_word = [item]
        answer = bigcilin_respond(key_word)
        if entity_recognition(answer):
            syn_list = get_synonym(answer)
            if len(syn_list) == 0:
                print("[entity recognition] {} is an entity but has no synonym.".format(item))
            else:
                print("[entity recognition] synonym of {} is {}.".format(item, syn_list))
                synonym_list.append(syn_list)
                for i in syn_list:
                    used_geo.add(i)
        else:
            print("[entity recognition] {} is not an entity.".format(item))
