#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response

from accounts import models as accounts_model
from assets import models as assets_model
from api import assets_searializer
from api import accounts_searializer

from backend import ApiAuth


class HostView(viewsets.ModelViewSet):
    queryset = assets_model.Host.objects.all()
    serializer_class = assets_searializer.HostSerializer


class RoleView(viewsets.ModelViewSet):
    queryset = accounts_model.Role.objects.all()
    serializer_class = accounts_searializer.RoleSerializer


class UserView(viewsets.ModelViewSet):
    queryset = accounts_model.UserProfile.objects.all()
    serializer_class = accounts_searializer.UserSerializer


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
# @ApiAuth.token_required
def HostList(request):
    if request.method == 'GET':
        asset_list = assets_model.Host.objects.all()
        serializer = assets_searializer.HostSerializer(asset_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = assets_searializer.HostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
# @ApiAuth.token_required   #/api/user_list/?name=pandonglin&timestamp=1487434393&token=ee87a8dee0
def UserList(request):
    if request.method == 'GET':
        asset_list = accounts_model.UserProfile.objects.all()
        serializer = accounts_searializer.UserSerializer(asset_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = accounts_searializer.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)