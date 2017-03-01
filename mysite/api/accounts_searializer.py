#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin

from accounts.models import UserProfile, Role
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("id", "name", "is_active", "is_admin", "department", "mobile", "role")
        depth = 2


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name", "perm")
        depth = 1