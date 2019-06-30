# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/6/15
@Author: Haojun Gao
@Description: 
"""

set = set()

set.add("a")
set.add("b")
set.add("c")

with open('geo_noun.txt', 'w') as f:
    for item in set:
        f.write(item + "\n")