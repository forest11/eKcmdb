#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin

from assets import models
from rest_framework import serializers


class HostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Host
        fields = ('sn', 'hostname','management_ip')   #api展示的字段
        depth = 2  #展示层级数
