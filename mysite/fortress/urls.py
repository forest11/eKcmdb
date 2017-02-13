# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django.conf.urls import url
from fortress import views

urlpatterns = [
    url(r'^show_message/', views.show_message, name='show_message'),
]
