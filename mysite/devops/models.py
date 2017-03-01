from django.db import models
from assets.models import Host
from accounts.models import UserProfile
from assets.models import BusinessUnit


class RemoteUser(models.Model):
    """主机用户"""
    auth_type_choices = (
        (0, 'ssh-password'),
        (1, 'ssh-key')
    )
    auth_type = models.SmallIntegerField(choices=auth_type_choices, default=0)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=256, help_text="如果auth_type选择为ssh-key,那此处就应该是key的路径")

    def __str__(self):
        return self.username

    class Meta:
        unique_together = ('auth_type', 'username', 'password')
        verbose_name = "远程用户"
        verbose_name_plural = verbose_name


class BindHost(models.Model):
    """
    主机与用户绑定
    """
    host = models.ForeignKey(Host)
    user = models.ManyToManyField(UserProfile)
    remote_user = models.ForeignKey('RemoteUser')

    def __str__(self):
        return "%s:%s" % (self.host.hostname, self.remote_user.username)

    class Meta:
        unique_together = ('host', 'remote_user')
        verbose_name = "主机与帐号绑定"
        verbose_name_plural = verbose_name


class HostGroups(models.Model):
    """
    主机组
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="名称")
    bind_hosts = models.ManyToManyField('BindHost', blank=True)
    user = models.ManyToManyField(UserProfile)
    memo = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "主机组"
        verbose_name_plural = verbose_name


class Task(models.Model):
    """
    任务
    """
    action_choices = (
        (0, 'cmd'),
        (1, 'file_transfer')
    )
    task_type = models.SmallIntegerField(choices=action_choices, verbose_name="执行类型")
    user = models.ForeignKey(UserProfile, verbose_name='堡垒机账号')
    bind_hosts = models.ManyToManyField('BindHost')
    task_detail = models.CharField(max_length=512)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s: %s" % (self.user.name, self.task_detail)

    class Meta:
        verbose_name = "任务"
        verbose_name_plural = verbose_name


class TaskDetail(models.Model):
    """
    任务日志
    """
    task = models.ForeignKey(Task)
    task_result_choices = (
        ('Success', 'Success'),
        ('Failed', 'Failed'),
        ('Processing', 'Processing'),
        ('Canceled', 'Canceled')
    )
    result = models.CharField(choices=task_result_choices, max_length=32, default='Processing', verbose_name="执行状态")
    bind_host = models.ForeignKey("BindHost")
    event_log = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.task.task_detail

    class Meta:
        unique_together = ('task', 'bind_host')
        verbose_name = "任务日志"
        verbose_name_plural = verbose_name


class Code(models.Model):
    """
    代码发布
    """
    status_choices = (
        (0, "等待审批中"),
        (1, "等待测试中"),
        (2, "已完成"),
        (3, "测试失败"),
        (4, "未知"),
    )
    name = models.CharField(max_length=256, unique=True, verbose_name="发布名称")
    introduce = models.TextField(verbose_name="发布说明")
    env = models.ForeignKey("Environment", verbose_name="发布环境")
    project = models.ForeignKey(BusinessUnit, verbose_name="项目名")
    version = models.CharField(max_length=32, verbose_name="版本号")
    pusher = models.ForeignKey(UserProfile, related_name="p", verbose_name="发布者")
    approver = models.ForeignKey(UserProfile, null=True, blank=True, related_name="a", verbose_name="审批者")
    tester = models.ManyToManyField(UserProfile, related_name="t", verbose_name="测试者")
    commit_time = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")
    approve_time = models.DateTimeField(null=True, blank=True, verbose_name="审核完成时间")
    push_time = models.DateTimeField(null=True, blank=True, verbose_name="发布完成时间")
    status = models.SmallIntegerField(choices=status_choices, default=4, verbose_name="发布状态")


class Environment(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "环境"
        verbose_name_plural = verbose_name


class CodeLog(models.Model):
    log = models.TextField(verbose_name="log")

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "日志"
        verbose_name_plural = verbose_name