from django.db import models


class BasicInfo(models.Model):
    """病人预约信息"""

    name = models.CharField(max_length=30)  # 姓名
    husband = models.CharField(max_length=30, default='')  # 丈夫
    age = models.SmallIntegerField(blank=True, null=True)  # 年龄
    sex = models.CharField(max_length=10, blank=True, null=True)  # 性别
    marriage = models.CharField(max_length=20, null=True)  # 婚姻状况
    address = models.CharField(max_length=80, blank=True, null=True)  # 现地址
    phone = models.CharField(max_length=13, blank=True, null=True)  # 病人家属电话
    department = models.CharField(max_length=23, blank=True, null=True)  # 科室名称
    department_arabic = models.CharField(max_length=33, default='', blank=True, null=True)  # 科室名称
    date = models.DateField(auto_now_add=True, blank=True, null=True)  # 登记时间
    order = models.SmallIntegerField(blank=True, null=True)  # 顺序
    timeOfArrival = models.CharField(max_length=7, blank=True, null=True)  # 到达时间

    def __str__(self):
        return self.name
