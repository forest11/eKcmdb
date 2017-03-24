#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from django import template
import json

register = template.Library()


@register.filter
def make_null(args):
    return ''


@register.filter
def json_obj(args):
    return json.loads(args)

