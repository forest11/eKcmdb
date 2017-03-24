#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
import json
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404
from backend.response import BaseResponse
from database import models


class MonitorDetail(View):

    def get(self, request):
        return render(request, 'default/index.html')

    def post(self, request):
        return render(request, 'default/index.html')


class ZabbixList(View):

    def get(self, request):
        return render(request, 'default/index.html')

    def post(self, request):
        return render(request, 'default/index.html')
