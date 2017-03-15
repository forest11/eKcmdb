#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
import json
import time
from django.conf import settings
from django.shortcuts import HttpResponse
from backend.response import BaseResponse
from accounts import models
from backend import GenerateMd5


def get_token(name, timestamp, token):
    token_format = "%s%s%s" % (name, timestamp, token)
    return GenerateMd5.generate_md5(token_format)[5:15]  #截断，


def token_required(func):
    """
    token认证装饰器
    ?name=pandonglin&timestamp=1487434393&token=ee87a8dee0
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        rep = BaseResponse()

        get_args = args[0].GET  #== request
        name = get_args.get("name")
        token_md5_from_client = get_args.get("token")
        timestamp = get_args.get("timestamp")

        if not name or not timestamp or not token_md5_from_client:
            rep.message = {"msg-error": [{"message": "name, timestamp, token is required"}]}
        else:
            try:
                user_obj = models.UserProfile.objects.get(name=name)
                token_md5_from_server = get_token(name, timestamp, user_obj.token)  #在服务端取出用户的toke截断码

                if token_md5_from_server != token_md5_from_client:
                    rep.message = {"msg-error": [{"message": "authentication failed"}]}
                else:
                    if abs(int(time.time()) - int(timestamp)) > settings.TOKEN_TIMEOUT:   #超时，防止多次被使用
                        rep.message = {"msg-error": [{"message": "authentication failed"}]}
                    else:
                        pass
            except Exception as e:
                print(str(e))
                rep.message = {"msg-error": [{"message": "the name does not exist"}]}
        if rep.message:
            return HttpResponse(json.dumps(rep.__dict__))
        else:
            return func(*args, **kwargs)

    return wrapper
