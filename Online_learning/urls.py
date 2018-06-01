"""Online_learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # 等同于在django.conf.urls导入include
from django.conf.urls import url
import xadmin

from users.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    # path('admin/', admin.site.urls),
    path('admin/', xadmin.site.urls),
    path('captcha/', include('captcha.urls')),

    # # 用户操作管理，URL
    # url(r'^opera/', include('apps.operation.urls', namespace='opera')),
    # # 课程机构相关 URL
    # url(r'^org/', include('apps.organizations.urls', namespace='org')),
    # # 课程相关 URL 配置
    # url(r'^course/', include('apps.courses.urls', namespace='courses')),

    # 用户中心 URL 配置,看include源码进行配置，默认app_name=None,只有为元组时才能传入参数
    path('users/', include(('users.urls', 'users'), namespace='users')),

]
