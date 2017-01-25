from django.contrib import admin
from autoops import models

admin.site.register(models.RemoteUser)
admin.site.register(models.BindHost)
admin.site.register(models.HostGroups)
admin.site.register(models.Task)
admin.site.register(models.TaskDetail)
