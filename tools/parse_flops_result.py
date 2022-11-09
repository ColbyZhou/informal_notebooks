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
Date:   2022/08/10 16:27:05
"""
import sys

def convert(num_str):
    if "m" in num_str:
        num_str = num_str.replace('m', '')
        val = float(num_str) * 1000000
    elif "k" in num_str:
        num_str = num_str.replace('k', '')
        val = float(num_str) * 1000
    else:
        val = float(num_str)
    return val

def de_convert(num):
    if num > 1000000:
        return "{:.2f}".format(num / 1000000) + 'm'
    elif num > 1000:
        return "{:.2f}".format(num / 1000) + 'k'
    else:
        return "{:.2f}".format(num)

val_dict = dict()
grad_dict = dict()

with open(sys.argv[1], 'r') as file:
    for line in file:
        line = line.strip("\r\n")
        space_count = 0
        for ch in line:
            if ch == ' ':
                space_count += 1
            else:
                break

        if space_count != 2 and space_count != 0:
            continue

        line = line.strip()
        line = line.replace("mmoe_scope/", "")

        is_grad = False
        if 'gradients' in line:
            line = line.replace("gradients/", "")
            is_grad = True
            #continue

        if '_TFProfRoot' in line:
            name = '_TFProfRoot'
            #continue
        else:
            name = line.split("/")[0]

        if name.split("_")[-1].isdigit():
            name = "_".join(name.split("_")[:-1])

        if 'care_bottomSTAR' in name:
            name = 'star_domain_task_for_care'
        if 'MMOE_original' in name:
            name = 'MMOE_original'
        if 'memory_block' in name:
            name = 'build_memory_augment_components'

        flops_str = line.split("(")[-1].split(' ')[0].split("/")[1]
        if name not in val_dict:
            val_dict[name] = convert(flops_str)
        else:
            val_dict[name] += convert(flops_str)

        if is_grad:
            if name not in grad_dict:
                grad_dict[name] = convert(flops_str)
            else:
                grad_dict[name] += convert(flops_str)

        #print name + "\t" + flops_str


total = val_dict["_TFProfRoot"]
sorted_items = sorted(val_dict.items(), key=lambda x:x[1], reverse=True)
for key, val in sorted_items:
    if key in grad_dict:
        grad_val = grad_dict[key]
    else:
        grad_val = 0
    print("\t".join([key, de_convert(val), str(val), "{:.4f}".format(val / total), de_convert(grad_val), str(grad_val)]))
    #print("\t".join([key, de_convert(val), "{:.4f}".format(val / total)]))

