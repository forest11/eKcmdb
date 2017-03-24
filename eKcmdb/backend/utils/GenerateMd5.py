#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
import hashlib
import time


def generate_salt_md5(value):
    """
    根据值根据时间加盐生成md5值
    :param value:
    :return:
    """
    time_str = str(time.time())
    obj = hashlib.md5(time_str.encode('utf-8'))
    obj.update(value.encode('utf-8'))
    return obj.hexdigest()


def generate_md5(value):
    """
    根据值生成md5值
    :param value:
    :return:
    """
    obj = hashlib.md5()
    obj.update(value.encode('utf-8'))
    return obj.hexdigest()
