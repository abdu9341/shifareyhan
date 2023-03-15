from django.conf.urls import url
from user import views

urlpatterns = [

    # 登录页面
    url(r'^login/$', views.login),
    url(r'^loginCheck/$', views.loginCheck, name='loginCheck'),
    url(r'^logout/$', views.logout),

    # 账户资料
    url(r'^profileAdmin/$', views.profileAdmin, name='profileAdmin'),
    url(r'^editAdminProfile/(\d+)$', views.editAdminProfile, name='editAdminProfile'),

]
