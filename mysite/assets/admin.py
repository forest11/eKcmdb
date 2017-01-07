from django.contrib import admin
from assets import models

admin.site.register(models.Host)
admin.site.register(models.BusinessUnit)
admin.site.register(models.IDC)
admin.site.register(models.System)
admin.site.register(models.CPU)
admin.site.register(models.RAM)
admin.site.register(models.Disk)
admin.site.register(models.NIC)
admin.site.register(models.Manufactory)
admin.site.register(models.Service)
admin.site.register(models.Device)