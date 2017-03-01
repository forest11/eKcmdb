#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from django.shortcuts import render
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class CheckUserAuth(MiddlewareMixin):
    public_url = settings.PUBLIE_URL

    def process_request(self, request):
        perm_list = request.session.get('perm_list')
        if perm_list:
            if request.path_info == "/favicon.ico" or request.path_info.startswith(
                    "/admin") or request.path_info.startswith("/api") or request.path_info.startswith("/static"):
                pass
            else:
                try:
                    cur_url = request.path_info.split('/')[2]
                    if cur_url not in perm_list and cur_url not in CheckUserAuth.public_url:
                        return render(request, 'common/403.html', status=403)
                except:
                    pass
