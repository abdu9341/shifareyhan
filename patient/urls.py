from django.conf.urls import url
from patient import views

urlpatterns = [

    url(r'reservation/$', views.reservation, name='reservation'),  # 预订


    url(r'^newAppointment/$', views.newAppointment, name='newAppointment'),  # 添加预约

    url(r'^result/(\d+)$', views.result, name='result'),  # 结果
    url(r'^editAppointment/(\d+)$', views.editAppointment, name='editAppointment'),  # 编辑


    # 通知
    url(r'^notification/$', views.notification, name='notification'),


    # 门诊时间表
    url(r'', views.polyclinicTimeForPatient, name='polyclinicTimeForPatient'),


]
