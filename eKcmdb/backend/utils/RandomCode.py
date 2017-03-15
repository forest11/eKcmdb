#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
import random


def random_code(n):
    """
    n位数随机字符串
    :return:
    """
    code = ''
    _letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
    _upper_cases = _letter_cases.upper()  # 大写字母
    _numbers = ''.join(map(str, range(3, 10)))  # 数字
    init_chars = ''.join((_letter_cases, _upper_cases, _numbers)) #组成混合字符串
    for i in range(n):
        code += init_chars[random.randint(0, len(init_chars)-1)]
    return code
