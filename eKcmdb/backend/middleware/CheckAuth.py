#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from backend.utils import ResolveUrl
from django.urls import reverse as url_reverse


class CheckUserAuth(MiddlewareMixin):
    public_url = settings.PUBLIE_URL

    def process_request(self, request):
        if request.path_info == "/favicon.ico" or request.path_info.startswith(
                "/admin") or request.path_info.startswith("/api") or request.path_info.startswith("/static"):
            pass
        elif request.path_info in ResolveUrl.url(CheckUserAuth.public_url):
            pass
        elif request.user == 'AnonymousUser':
            return redirect(url_reverse('login'))
        else:
            cur_url = request.path_info
            perm_list = request.session.get('perm_list')
            if perm_list:

                if cur_url not in ResolveUrl.url(perm_list):
                    return render(request, 'default/403.html', status=403)
            else:
                return render(request, 'default/403.html', status=403)
