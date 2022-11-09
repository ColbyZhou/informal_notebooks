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
Date:   2021/06/18 19:45:20
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import math
import random

sess = tf.Session()

#y = tf.Variable(2.0)
x = tf.Variable(1.5)

a = tf.constant(3.0)
b = tf.constant(1.0)

y_1 = a * x + b
g = tf.gradients(y_1, x)
g_n = tf.norm(g, ord=2)

print(a)
print(b)
print(x)
print(y_1)
print(g)
print(g_n)

print(sess.run(g))
print(sess.run(g_n))
