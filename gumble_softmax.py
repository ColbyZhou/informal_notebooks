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
Date:   2021/07/01 16:53:46
"""

from scipy.optimize import curve_fit

import math
import numpy as np
from matplotlib.pyplot import *
import tensorflow as tf



sess = tf.Session()

############## 1. define a distribution
mean = tf.Variable(2.)
idxs = tf.Variable([0., 1., 2., 3., 4.], trainable=False)
# An unnormalised approximately-normal distribution
logits = tf.exp(-(idxs - mean) ** 2)

def print_logit_vals():
    logit_vals = sess.run(logits)
    print(" ".join(["{:.2f}"] * len(logit_vals)).format(*logit_vals))

sess.run(tf.global_variables_initializer())
print("Logits: ")
print_logit_vals()


############## 2. define sampling process graph
def differentiable_sample(logits):
    noise = tf.random_uniform(tf.shape(logits))
    logits_with_noise = logits - tf.log(-tf.log(noise))
    return tf.nn.softmax(logits_with_noise)

sample = differentiable_sample(logits)
sample_weights = tf.Variable([1., 2., 3., 4., 5.], trainable=False)
############## 3. get soft one-hot output, which approximates argmax one-hot output
result = tf.reduce_sum(sample * sample_weights)


############## 4. try back-propagate
sess.run(tf.global_variables_initializer())
train_op = tf.train.GradientDescentOptimizer(learning_rate=1).minimize(-result)

print("Distribution mean: {:.2f}".format(sess.run(mean)))
for i in range(5):
    sess.run(train_op)
    result_val, mean_val, idxs_val, sample_weights_val = sess.run([result, mean, idxs, sample_weights])
    print("result_val: {:.2f}".format(result_val))
    print("Distribution mean: {:.2f}".format(mean_val))
    print("idxs_val:")
    print(idxs_val)
    print("sample_weights_val:")
    print(sample_weights_val)

