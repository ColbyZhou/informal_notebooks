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
Date:   2021/07/01 13:41:28
"""

from scipy.optimize import curve_fit

import math
import numpy as np
from matplotlib import pyplot as plt


mean_hunger = 5
samples_per_day = 100
n_days = 10000
samples = np.random.normal(loc=mean_hunger, size=(n_days, samples_per_day))
daily_maxes = np.max(samples, axis=1)

def gumbel_pdf(prob, loc, scale):
    z = (prob - loc) / scale
    return np.exp(-z - np.exp(-z)) / scale

def plot_maxes(daily_maxes):
    print(daily_maxes)
    probs, hungers, _ = plt.hist(daily_maxes, normed=True, bins=100)
    s = sum(probs)
    print(probs)
    print(s)
    print(len(probs))
    print(len(hungers))
    print(hungers)
    plt.xlabel("Hunger")
    plt.ylabel("Probability of hunger being daily maximum")

    (loc, scale), _ = curve_fit(gumbel_pdf, hungers[:-1], probs)
    print(loc)
    print(scale)
    plt.plot(hungers, gumbel_pdf(hungers, loc, scale))
    plt.legend()
    plt.show()

plt.figure()
print(daily_maxes)
plot_maxes(daily_maxes)

