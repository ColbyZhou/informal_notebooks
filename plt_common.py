#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# Copyright (c) 2022 www.tencent.com, Inc. All Rights Reserved
#
################################################################################

"""
This module provide service.

Author: zhouqiang
Date:   2022/12/29 17:11:51
"""

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_hist(path, idx, left, right, bin, non_zero=False, splitter="\t"):
    val_list = []
    non_zero_cnt = 0
    ttl = 0
    with open(path, 'r') as f:
        for line in f:
            fs = line.strip().split(splitter)
            value = float(fs[idx])
            if not non_zero_cnt or value > 0:
                non_zero_cnt += 1
                val_list.append(value)
            ttl += 1
    plt.figure(figsize = (12,9))
    plt.title(path.split("/")[-1])

    n, bins, _ = plt.hist(val_list, density=False, range=(left, right), bins=bin)

    sum_n = sum(n)
    normed_n = n * 1.0000 / sum_n
    r = sum_n * 1.0000 / len(val_list)
    print("effective data count:" + str(sum_n))
    print("total data count:" + str(len(val_list)))
    print("effective data ratio:" + "{:.2f}%".format(r * 100))

    if non_zero:
        print("non zero: " + str(non_zero_cnt) + ", total: " + str(ttl) + ", ratio: " + str(non_zero_cnt * 1.00 / ttl))

    [print("{:.3f}".format(k) + ": " + "{:.2f}%".format(x * 100)) for k, nn, x in list(zip(bins, n, normed_n))[:bin]]

    plt.show()

