from django.db import models


class User(models.Model):
    """用户信息"""

    name = models.CharField(max_length=25)  # 姓名
    account = models.CharField(max_length=3, unique=True, null=True, blank=True)
    password = models.CharField(max_length=9)  # 密码
    # 权限：1表示高级管理员，2 表示预约者
    authority = models.SmallIntegerField(null=True, blank=True)
    isEdit = models.BooleanField(default=False, blank=True)  # False表示不编辑， True表示编辑

    def __str__(self):
        return self.name
