from django.conf.urls import url
from clinic import views

urlpatterns = [

    # 门诊科室表
    url(r'^polyclinicDepartment/$', views.polyclinicDepartment, name='polyclinicDepartment'),
    url(r'^addDepartment/$', views.addDepartment, name='addDepartment'),
    url(r'^editDepartment/(\d+)$', views.editDepartment, name='editDepartment'),  # 编辑门诊科室
    url(r'^activeDepartment/(\d+)$', views.activeDepartment, name='activeDepartment'),  # 激活门诊科室
    url(r'^inactiveDepartment/(\d+)$', views.inactiveDepartment, name='inactiveDepartment'),  # 未激活门诊科室
    url(r'^deleteDepartment/(\d+)$', views.deleteDepartment, name='deleteDepartment'),  # 删除门诊科室

    # 门诊科室排班表
    url(r'^polyclinicTimeForAdmin/$', views.polyclinicTimeForAdmin, name='polyclinicTimeForAdmin'),

    # 门诊排班
    url(r'^addSchedule/$', views.addSchedule, name='addSchedule'),  # 添加门诊时间
    url(r'^editSchedule/(\d+)$', views.editSchedule, name='editSchedule'),  # 编辑门诊时间
    url(r'^deleteSchedule/(\d+)$', views.deleteSchedule, name='deleteSchedule'),  # 删除门诊时间
    url(r'^openSchedule/(\d+)$', views.openSchedule, name='openSchedule'),  # 开启排班
    url(r'^closeSchedule/(\d+)$', views.closeSchedule, name='closeSchedule'),  # 关闭排班

    # 预订
    url(r'^reservationAdmin/$', views.reservationAdmin, name='reservationAdmin'),
    url(r'^newAppointmentAdmin/$', views.newAppointmentAdmin, name='newAppointmentAdmin'),  # 添加预约
    url(r'^resultAdmin/(\d+)$', views.resultAdmin, name='resultAdmin'),  # 结果
    url(r'^editAppointmentAdmin/(\d+)$', views.editAppointmentAdmin, name='editAppointmentAdmin'),  # 编辑

    # 系统时间
    url(r'^systemTime/$', views.systemTime, name='systemTime'),
    url(r'^openEditSystemTime/(\d+)$', views.openEditSystemTime, name='openEditSystemTime'),
    url(r'^editSystemTime/(\d+)$', views.editSystemTime, name='editSystemTime'),
    url(r'^openSystem/(\d+)$', views.openSystem, name='openSystem'),
    url(r'^closeSystem/(\d+)$', views.closeSystem, name='closeSystem'),


    # 通知
    url(r'^notificationAdmin/$', views.notificationAdmin, name='notificationAdmin'),
    url(r'^addNotification/$', views.addNotification, name='addNotification'),
    url(r'^editNotification/(\d+)$', views.editNotification, name='editNotification'),

    #  删除通知
    url(r'^deleteNotification/(\d+)$', views.deleteNotification, name='deleteNotification'),


    url(r'^excel/', views.excel, name='excel'),  #
    url(r'^toExcel/$', views.toExcel, name='toExcel'),  # 下载excel文档

]
