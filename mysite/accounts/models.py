from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from backend import RandomCode


class CheckCode(models.Model):
    """
    验证码临时表
    """
    email = models.CharField(max_length=32, db_index=True)
    code = models.CharField(max_length=12)
    times = models.IntegerField(default=1)
    ctime = models.DateTimeField()


class UserProfileManager(BaseUserManager):
    """
    用户管理
    """
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    """
    用户表
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name="管理员")
    name = models.CharField(max_length=32, verbose_name="姓名")
    token = models.CharField(max_length=128, blank=True, null=True, verbose_name='用户token')
    user_key = models.CharField(max_length=100, default=RandomCode.random_code(100), verbose_name='用户key')
    department = models.CharField(max_length=32, blank=True, null=True, verbose_name='部门')
    tel = models.CharField(max_length=32, blank=True, null=True, verbose_name='座机')
    mobile = models.CharField(max_length=32, blank=True, null=True,  verbose_name='手机')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    # groups = models.ManyToManyField('Group')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserProfileManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email
