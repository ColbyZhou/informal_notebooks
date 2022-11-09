#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# Copyright (c) 2022 tencent.com, Inc. All Rights Reserved
#
################################################################################

"""
This module provide service.

Author: 
Date:   2022/08/10 15:57:02
"""
#import tensorflow.compat.v1 as tf
import tensorflow as tf

print(tf.__version__)
from google.protobuf import text_format


def stats_graph(graph):
    flops = tf.profiler.profile(graph, options=tf.profiler.ProfileOptionBuilder.float_operation())
    params = tf.profiler.profile(graph, options=tf.profiler.ProfileOptionBuilder.trainable_variables_parameter())
    print('FLOPs: {};    Trainable params: {}'.format(flops.total_float_ops, params.total_parameters))


# data_file = 'ynews_rank_merge_0628_v1-dense-2022_08_09_111719-complete.pbtxt'
data_file = 'ynews_rank_colby_flops_opt_test_1-dense-2022_08_10_135259-complete.pbtxt'

with open(data_file, 'rb') as f:
    #graph_def = tf.compat.v1.GraphDef()
    graph_def = tf.GraphDef()
    text_format.Parse(f.read(), graph_def)

with tf.Graph().as_default() as graph:
    tf.import_graph_def(graph_def, name='')
    stats_graph(graph)

