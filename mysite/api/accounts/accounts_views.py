#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from api.accounts import accounts_searializer
from accounts import models


class UserView(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = accounts_searializer.UserSerializer


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def UserList(request):
    if request.method == 'GET':
        asset_list = models.UserProfile.objects.all()
        serializer = accounts_searializer.UserSerializer(asset_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = accounts_searializer.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
