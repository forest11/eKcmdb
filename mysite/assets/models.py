from django.db import models
from accounts.models import UserProfile


class Host(models.Model):
    device_type_choices = (
        (0, "Dell R510"),
        (1, "Dell R620"),
        (2, "Dell R710"),
        (3, "Dell R720"),
        (4, "Dell R720xd"),
        )

    raid_type_choices = (
        (0, 'RADI 0'),
        (1, 'RADI 1'),
        (2, 'RADI 5'),
        (3, 'RADI 10'),
    )
    status_choices = (
        (0, "在线"),
        (1, "下线"),
        (2, "故障"),
        (3, "备用"),
        (4, "未知"),
    )
    ip = models.GenericIPAddressField(unique=True, verbose_name='IP')
    hostname = models.CharField(max_length=64, null=True, blank=True, verbose_name="主机名")
    sn = models.CharField(max_length=64, null=True, blank=True, verbose_name="sn")
    number = models.CharField(max_length=64, null=True, blank=True, verbose_name='资产编号')
    qs = models.CharField(max_length=64, null=True, blank=True, verbose_name="快速服务代码")
    asset_name = models.SmallIntegerField(choices=device_type_choices, default=3, verbose_name='设备名称')
    os_type = models.ForeignKey('System', null=True, blank=True, verbose_name="操作系统")
    manufactory = models.ForeignKey('Manufactory', null=True, blank=True, verbose_name="制造厂商")
    raid_type = models.SmallIntegerField(choices=raid_type_choices, default=3, verbose_name="RAID类型")
    management_ip = models.GenericIPAddressField(unique=True, null=True, blank=True, verbose_name='管理IP')
    idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name='IDC机房')
    cabinet = models.CharField(max_length=32, null=True, blank=True, verbose_name='机柜号')
    host_cabinet_id = models.CharField(max_length=32, null=True, blank=True, verbose_name='机器位置')
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="设备状态")
    is_virtual = models.BooleanField(default=False, verbose_name="虚拟机")
    parent_host = models.ForeignKey('self', related_name='parent_level', null=True, blank=True, verbose_name="宿主机")
    admin = models.CharField(max_length=32, null=True, blank=True, verbose_name='资产管理员')
    buy_date = models.DateField(null=True, blank=True, verbose_name="购买时间")
    create_date = models.DateTimeField(blank=True, auto_now_add=True, verbose_name="创建时间")
    update_date = models.DateTimeField(blank=True, auto_now=True, verbose_name="最近修改时间")
    memo = models.TextField(null=True, blank=True, verbose_name='备注')

    class Meta:
        verbose_name = "主机"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s sn:%s" % (self.hostname, self.sn)


class NetDevice(models.Model):
    device_type_choices = (
        (0, '交换机'),
        (1, '路由器'),
        (2, '防火墙'),
        (3, '安全设备'),
    )
    status_choices = (
        (0, "在线"),
        (1, "下线"),
        (2, "故障"),
        (3, "备用"),
        (4, "未知"),
    )
    sn = models.CharField(max_length=64, verbose_name="sn")
    ip = models.GenericIPAddressField(unique=True, verbose_name='IP')
    number = models.CharField(max_length=32, null=True, blank=True, verbose_name='资产编号')
    qs = models.CharField(max_length=64, null=True, blank=True, verbose_name="快速服务代码")
    asset_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='设备名称')
    asset_type = models.SmallIntegerField(choices=device_type_choices, default=0, verbose_name="设备类型")
    manufactory = models.ForeignKey('Manufactory', null=True, blank=True, verbose_name="制造厂商")
    idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name='IDC机房')
    cabinet = models.CharField(max_length=32, null=True, blank=True, verbose_name='机柜号')
    device_cabinet_id = models.CharField(max_length=32, null=True, blank=True, verbose_name='机器位置')
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="设备状态")
    parent_device = models.ForeignKey('self', related_name='parent_level', null=True, blank=True, verbose_name="上链设备")
    admin = models.CharField(max_length=32, null=True, blank=True, verbose_name='资产管理员')
    buy_date = models.DateField(null=True, blank=True, verbose_name="购买时间")
    create_date = models.DateTimeField(blank=True, auto_now_add=True, verbose_name="创建时间")
    update_date = models.DateTimeField(blank=True, auto_now=True, verbose_name="最近修改时间")
    memo = models.TextField(null=True, blank=True, verbose_name='备注')

    class Meta:
        verbose_name = "网络设备"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s sn:%s" % (self.asset_name, self.sn)


class IDC(models.Model):
    name = models.CharField(max_length=64, verbose_name='IDC名称')
    staff = models.CharField(max_length=32, verbose_name='客服')
    phone = models.CharField(max_length=32, verbose_name="IDC联系电话")
    address = models.CharField(max_length=128, verbose_name="IDC地址")
    memo = models.CharField(max_length=128, null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'staff')
        verbose_name = 'IDC'
        verbose_name_plural = verbose_name


class System(models.Model):
    system_os_choice = (
        (0, "Centos"),
        (1, "Window"),
    )
    name = models.SmallIntegerField(choices=system_os_choice, default=0, verbose_name="系统类型")
    version = models.CharField(max_length=32, verbose_name="系统版本号")

    def __str__(self):
        if self.name == 0:
            return "Centos %s" % self.version
        else:
            return "Window %s" % self.version

    class Meta:
        verbose_name = "操作系统"
        verbose_name_plural = verbose_name


class CPU(models.Model):
    host = models.OneToOneField('Host', related_name='cpu')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU型号')
    cpu_count = models.SmallIntegerField('物理CPU个数')
    cpu_core_count = models.SmallIntegerField('CPU核数')

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.model


class RAM(models.Model):
    host = models.ForeignKey('Host', related_name='ram')
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name='SN号')
    model = models.CharField(max_length=128, verbose_name='型号')
    slot = models.CharField(max_length=64, blank=True, null=True, verbose_name='插槽')
    capacity = models.IntegerField('内存大小(MB)')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")

    auto_create_fields = ['sn', 'slot', 'model', 'capacity']

    class Meta:
        verbose_name = '内存'
        verbose_name_plural = verbose_name
        unique_together = ("host", "slot")

    def __str__(self):
        return '资产:%s, 插槽:%s, 容量:%s' % (self.host_id, self.slot, self.capacity)


class Disk(models.Model):
    host = models.ForeignKey('Host', related_name='disk')
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name='SN号')
    slot = models.CharField(max_length=64, blank=True, null=True, verbose_name='插槽位')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='磁盘型号')
    capacity = models.FloatField('磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )
    iface_type = models.CharField(choices=disk_iface_choice, max_length=64, default='SAS', verbose_name='接口类型')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")

    auto_create_fields = ['sn', 'slot', 'model', 'capacity', 'iface_type']

    class Meta:
        unique_together = ("host", "slot")
        verbose_name = '硬盘'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '资产:%s, 插槽:%s, 容量:%s' % (self.host_id, self.slot, self.capacity)


class Manufactory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='制造厂商')
    staff = models.CharField(max_length=32, blank=True, null=True, verbose_name='售后联系方式')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '制造厂商'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Service(models.Model):
    host = models.ManyToManyField('Host')
    name = models.CharField(max_length=64, verbose_name='服务名')
    port = models.IntegerField(verbose_name="端口")
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '服务'
        verbose_name_plural = verbose_name
        unique_together = ("name", "port")

    def __str__(self):
        return "%s:%s" % (self.name, self.port)


class BusinessUnit(models.Model):
    service = models.ManyToManyField('Service')
    name = models.CharField(max_length=64, unique=True, verbose_name='业务线')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = verbose_name