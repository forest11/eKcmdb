# -*- coding: utf-8 -*-
# __Author__: PanDongLin


class StatusCodeEnum:
    Failed = 500
    AuthFailed = 1001
    ArgsError = 1002
    Success = 200


class BaseResponse:
    def __init__(self):
        self.status = False
        # self.code = StatusCodeEnum.Success
        self.data = None
        self.message = {}
