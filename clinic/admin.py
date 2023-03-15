from django.contrib import admin
from clinic.models import *


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'arabic_name', 'saturday', 'sunday',
                    'monday', 'tuesday', 'wednesday', 'thursday']


class WeekAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'arabic_name', 'day_num']


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'department', 'week', 'start', 'end', 'time', 'quantity', 'count']


class SystemAdmin(admin.ModelAdmin):
    list_display = ['id', 'start', 'end', 'status']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text']


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(System, SystemAdmin)
