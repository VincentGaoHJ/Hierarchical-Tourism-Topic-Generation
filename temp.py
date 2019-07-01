# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/6/15
@Author: Haojun Gao
@Description: 
"""

import numpy as np

data = ['a', 'b', 'c', 'a', 'a', 'b', 'd']


# 计算信息熵的方法
def calc_ent(data):
    """
        calculate shanno ent of x
    """

    x = np.array(data)
    x_value_list = set([x[i] for i in range(x.shape[0])])
    ent = 0.0
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]
        logp = np.log2(p)
        ent -= p * logp

    print(ent)


calc_ent(data)
