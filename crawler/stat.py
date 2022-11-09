#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# Copyright (c) 2021 www.tencent.com, Inc. All Rights Reserved
#
################################################################################

"""
This module provide service.

Author: zhouqiang
Date:   2021/08/30 16:51:35
"""

import sys
import collections

reload(sys)
sys.setdefaultencoding('utf-8')

path = sys.argv[1]

stat_dict = dict()

with open(path, "r") as file:
    for line in file:
        line = line.strip()
        fs = line.split('\t')
        if len(fs) < 2:
            continue
        shiwen = fs[1]
        if len(shiwen) == 0:
            continue
        shiwen = shiwen.decode("utf-8")
        #print(type(shiwen))
        #print(len(shiwen))
        for word in shiwen:
            get = False
            code = ord(word)
            if code > 0x6C20 and code < 0x7040: # shui
            #if code > 0x6720 and code < 0x6B00: # mu
            #if code > 0x8260 and code < 0x8620: # cao
            #if code > 0x7AE0 and code < 0x7C60: # zhu
            #if code > 0x5FC0 and code < 0x6200: # xin
                get = True
            if not get:
                continue
            text = word.encode("utf-8")
            #print(text)
            if text not in stat_dict:
                stat_dict[text] = 0
            stat_dict[text] += 1


sorted_items = sorted(stat_dict.items(), key = lambda x:x[1], reverse = True)
for key, val in sorted_items:
    #print("key: %s, val: %d" % (key, val))
    print("%s\t%d" % (key, val))

