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
Date:   2021/07/04 15:37:16
"""

from scipy.optimize import curve_fit

import math
import copy
import numpy as np
from matplotlib.pyplot import *

n_samples = 1000

n_cats = 7
cats = np.arange(n_cats)

probs = np.random.randint(low=15, high=20, size=n_cats)
ori_probs = copy.deepcopy(probs)
print(probs)
probs = np.array(map(float, probs))
probs = probs / sum(probs)
print(probs)
#logits = np.log(probs)

def plot_probs(p, t = None):
    bar(cats, p)
    if t == None:
        xlabel("Category")
    else:
        xlabel(t)
    ylabel("Probability")

def argmax_probs(p):
    sample = np.argmax(p)
    one_hot = list(np.eye(len(p))[sample])
    print(type(one_hot))
    return one_hot

def softmax_probs(p, temp):
    p_with_t = p / temp
    p_with_t = p_with_t - p_with_t.max()
    exps = np.exp(p_with_t)
    preds = exps / np.sum(exps)
    return preds

print("*"*100)
figure()
subplot(2, 4, 1)
plot_probs(probs)
subplot(2, 4, 2)
plot_probs(ori_probs)
subplot(2, 4, 3)
argmax_sample = argmax_probs(ori_probs)
print(argmax_sample)
plot_probs(argmax_sample)
############ soft max with temperature
temps = [1.0, 0.5, 0.1, 0.01, 0.001]
for i in range(len(temps)):
    subplot(2, 4, 4 + i)
    softmax_sample = softmax_probs(ori_probs, temps[i])
    print("temp: " + str(temps[i]))
    print(softmax_sample)
    plot_probs(softmax_sample, "temp: " + str(temps[i]))


legend()
show()


