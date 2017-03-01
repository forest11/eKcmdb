# -*- coding: utf-8 -*-
# __Author__: PanDongLin


class StatusCodeEnum:
    Failed = 1000
    AuthFailed = 1001
    ArgsError = 1002
    Success = 2000


class BaseResponse:
    def __init__(self):
        self.status = False
        self.code = StatusCodeEnum.Success
        self.data = None
        self.message = {}
