"""eKcmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

handler404 = 'accounts.views.response_404_handler'


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('web.control.accounts_url')),
    url(r'^assets/', include('web.control.assets_url')),
    url(r'^devops/', include('web.control.devops_url')),
    url(r'^monitor/', include('web.control.monitor_url')),
    url(r'^favicon.ico$', RedirectView.as_view(url=r'static/img/favicon.ico')),
]