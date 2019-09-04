# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/9/3
@Author: Haojun Gao
@Description:
"""

import json
import math
import random
import requests
import threading

import telnetlib


# 继承父类 threading.Thread
class myThread(threading.Thread):
    def __init__(self, threadID, name, counter, proxies):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.proxies = proxies

    # 把要执行的代码写到 run 函数里面 线程在创建后会直接运行 run 函数
    def run(self):
        print("Starting " + self.name)
        proxy_json = json.loads(self.proxies)
        host = proxy_json['host']
        port = proxy_json['port']
        type = proxy_json['type']
        proxy = get_proxy(host, port, type)
        try:
            requests.get('https://cn.tripadvisor.com/', proxies=proxy, timeout=10)
        except:
            self.result = ""
        else:
            self.result = proxy
        print("Exiting " + self.name)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def multi_threading(proxies_list):
    threads = []
    thread_num = len(proxies_list)
    nloops = range(thread_num)

    for i in nloops:
        t = myThread(i, "Thread-" + str(i), i, proxies_list[i])
        threads.append(t)

    for i in nloops:  # start threads 此处并不会执行线程，而是将任务分发到每个线程，同步线程。等同步完成后再开始执行start方法
        threads[i].start()

    for i in nloops:  # jion()方法等待线程完成
        threads[i].join()

    return threads


def get_proxy(host, port, type):
    """
    构建格式化的单个proxies
    """
    if type == "http":
        proxy_ip = 'http://' + str(host) + ':' + str(port)
    else:
        proxy_ip = 'https://' + str(host) + ':' + str(port)
    proxy = {type: proxy_ip}
    return proxy


def getProxy(num):
    proxy_url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
    print("[Get_IP]URL:", proxy_url)

    response = requests.get(proxy_url)
    proxies_list = response.text.split('\n')
    print("[Get_IP]The number of IPs: ", len(proxies_list))
    skip = random.randint(1, 20)

    threads_num = math.ceil(1.5 * num)
    print("[准备] 需爬取 {} 个代理，故开启 {} 个线程".format(num, threads_num))

    threads = multi_threading(proxies_list[skip:skip + threads_num])
    ip_list = []
    for thread in threads:
        ip = thread.get_result()
        if ip != "":
            ip_list.append(ip)
            print('[Get_IP]Valid IP.')
            print("[Get_Valid_IP]", ip)
        else:
            print('[Get_IP]Failed IP.')

    print(len(ip_list))
    if len(ip_list) >= num:
        return ip_list[:num]
    else:
        return ip_list


if __name__ == '__main__':
    num = 10
    ip_list = getProxy(num)
    for ip in ip_list:
        print(ip)
