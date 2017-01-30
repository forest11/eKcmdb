from django.contrib import admin
from accounts import custom_user_admin
from accounts import models


admin.site.register(models.Role)
admin.site.register(models.UserToRole)
admin.site.register(models.Permission)
admin.site.register(models.RoleToPermission)
