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
Date:   2021/07/01 15:38:51
"""

from scipy.optimize import curve_fit

import math
import numpy as np
from matplotlib.pyplot import *

n_samples = 1000

n_cats = 7
cats = np.arange(n_cats)

probs = np.random.randint(low=1, high=20, size=n_cats)
probs = np.array(map(float, probs))
probs = probs / sum(probs)
logits = np.log(probs)
big_logits = np.log(probs * 1000)

def plot_probs():
    bar(cats, probs)
    xlabel("Category")
    ylabel("Probability")

def plot_estimated_probs(samples):
    n_cats = np.max(samples) + 1
    estd_probs, _, _ = hist(samples,
                            bins=np.arange(n_cats + 1),
                            align='left',
                            edgecolor='white',
                            normed=True)
    xlabel("Category")
    ylabel("Estimated probability")
    return estd_probs

def print_probs(probs):
    print(" ".join(["{:.2f}"] * len(probs)).format(*probs))

def draw_pics(t):
    estd_probs = plot_estimated_probs(samples)
    tight_layout()
    title(t, horizontalalignment = 'center')
    print("Estimated probabilities" + t + ":\t")
    print_probs(estd_probs)

###### 0. original probs
figure()
subplot(2, 4, 1)
plot_probs()
print("Original probabilities:\t\t")
print_probs(probs)

###### 1. sample using choice
samples = np.random.choice(cats, p=probs, size=n_samples)
subplot(2, 4, 2)
draw_pics("sample using choice")

###### 2. sample with uniform noise
def uniform_noise_sample(logits):
    noise = np.random.uniform(size=len(logits))
    sample = np.argmax(logits + noise)
    return sample

samples = [uniform_noise_sample(logits) for _ in range(n_samples)]
subplot(2, 4, 3)
draw_pics("sample using uniform noise")

###### 3. sample with normal noise
def normal_noise_sample(logits):
    noise = np.random.normal(size=len(logits))
    sample = np.argmax(logits + noise)
    return sample

samples = [normal_noise_sample(logits) for _ in range(n_samples)]
subplot(2, 4, 4)
draw_pics("sample using normal noise")

###### 4. sample with gumble noise
def gumble_noise_sample(logits):
    noise = np.random.gumbel(size=len(logits))
    sample = np.argmax(logits + noise)
    return sample

samples = [gumble_noise_sample(logits) for _ in range(n_samples)]
subplot(2, 4, 5)
draw_pics("sample using gumble noise")

###### 5. sample with human-maded gumble noise
def made_gumble_noise_sample(logits):
    noise = -np.log(-np.log(np.random.uniform(size=len(logits))))
    sample = np.argmax(logits + noise)
    return sample

print("logits:")
print(logits)
samples = [made_gumble_noise_sample(logits) for _ in range(n_samples)]
subplot(2, 4, 6)
draw_pics("sample using human-made gumble noise")

print("big logits:")
print(big_logits)
samples = [made_gumble_noise_sample(big_logits) for _ in range(n_samples)]
subplot(2, 4, 7)
draw_pics("sample using human-made gumble noise, big logits")


legend()
show()
