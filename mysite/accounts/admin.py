from django.contrib import admin
from accounts import custom_user_admin
from accounts import models


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'perm')}),
    )

    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('perm',)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('caption', 'code', 'method', 'kwargs',)
    list_filter = ('code',)
    fieldsets = (
        (None, {'fields': ('caption', 'code', 'method', 'kwargs',)}),
    )

    search_fields = ('caption',)
    ordering = ('caption',)

admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Permission, PermissionAdmin)
