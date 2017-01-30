#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from api.assets import assets_searializer
from assets import models


class HostView(viewsets.ModelViewSet):
    queryset = models.Host.objects.all()
    serializer_class = assets_searializer.HostSerializer


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def HostList(request):
    if request.method == 'GET':
        asset_list = models.Host.objects.all()
        serializer = assets_searializer.HostSerializer(asset_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = assets_searializer.HostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
