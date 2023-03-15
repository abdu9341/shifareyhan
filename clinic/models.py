from django.db import models


class Week(models.Model):
    """星期表"""

    name = models.CharField(max_length=10)  # 日期名称
    arabic_name = models.CharField(max_length=15, default='')
    day_num = models.SmallIntegerField(default=0, blank=True, null=True)  # 前天是这周的第几天

    def __str__(self):
        return self.name


class Department(models.Model):
    """门诊科室表"""

    name = models.CharField(max_length=25)  # 科室名称
    arabic_name = models.CharField(max_length=35, default='')
    # 状态， False表示关闭这个科室的排班，True表示开启这个科室的排班
    status = models.BooleanField(default=True, null=True, blank=True)
    # False关闭该次排班，True开启该次排班
    saturday = models.BooleanField(default=False, null=True, blank=True)
    sunday = models.BooleanField(default=False, null=True, blank=True)
    monday = models.BooleanField(default=False, null=True, blank=True)
    tuesday = models.BooleanField(default=False, null=True, blank=True)
    wednesday = models.BooleanField(default=False, null=True, blank=True)
    thursday = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    """门诊排班表"""

    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)  # 科室
    week = models.ForeignKey(Week, on_delete=models.SET_NULL, blank=True, null=True)  # 排班日期
    quantity = models.SmallIntegerField(default=0, blank=True, null=True)  # 可预约数量
    start = models.CharField(max_length=5, blank=True, null=True)  # 门诊开始时间
    end = models.CharField(max_length=5, blank=True, null=True)  # 门诊结束时间
    time = models.SmallIntegerField(blank=True, null=True)  # 看病时间， 单位：分钟
    # 状态， FALSE表示关闭该次排班，True表示开启该次排班
    status = models.BooleanField(default=True, null=True, blank=True)
    count = models.SmallIntegerField(default=0, blank=True, null=True)  # 当前科室已约的数量


class System(models.Model):
    """系统表"""

    start = models.SmallIntegerField(default=17, blank=True, null=True)  # 预约开始时间
    end = models.SmallIntegerField(default=19, blank=True, null=True)  # 预约结束时间
    # 状态， FALSE表示关闭系统，True表示开启系统
    status = models.BooleanField(default=True, null=True, blank=True)
    isEdit = models.BooleanField(default=False, blank=True)  # False表示不编辑， True表示编辑


class Notification(models.Model):
    """通知"""

    title = models.CharField(max_length=70, null=True, blank=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
