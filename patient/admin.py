from django.contrib import admin
from patient.models import BasicInfo


class BasicInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age', 'sex', 'order', 'timeOfArrival',
                    'phone', 'department', 'department_arabic', 'date']


admin.site.register(BasicInfo, BasicInfoAdmin)


