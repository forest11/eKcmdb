#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin

from accounts import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ("id", "name", "is_active", "is_admin", "mobile", "role")
        depth = 1