from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from backend.form import UserForm
from database import models


class UserAdmin(BaseUserAdmin):
    form = UserForm.UserChangeForm
    add_form = UserForm.UserCreationForm

    list_display = ('name', 'email', 'mobile', 'is_admin', 'memo')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('name', 'password')}),
        ('user info', {'fields': ('email', 'token', 'tel', 'mobile', 'is_active',)}),
        ('permissions', {'fields': ('is_admin', 'role',)}),
        ('other options', {'classes': ('collapse',),
                           'fields': ('last_login', 'memo',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2')
        }),
    )
    search_fields = ('name', 'email')
    ordering = ('name',)
    filter_horizontal = ()


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

admin.site.register(models.UserProfile, UserAdmin)
admin.site.unregister(Group)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.Host)
admin.site.register(models.BusinessUnit)
admin.site.register(models.IDC)
admin.site.register(models.System)
admin.site.register(models.CPU)
admin.site.register(models.RAM)
admin.site.register(models.Disk)
admin.site.register(models.Manufactory)
admin.site.register(models.Service)
admin.site.register(models.NetDevice)
admin.site.register(models.RemoteUser)
admin.site.register(models.BindHost)
admin.site.register(models.HostGroups)
admin.site.register(models.Task)
admin.site.register(models.TaskDetail)
admin.site.register(models.Code)
admin.site.register(models.CodeLog)
admin.site.register(models.Environment)
admin.site.register(models.SqlCheck)
admin.site.register(models.UrlCenter)

