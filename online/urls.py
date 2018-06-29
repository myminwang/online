"""online URL Configuration

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
from django.conf import settings
from django.views.static import serve  # 处理静态文件


from django.contrib import admin
from django.urls import path, include  # 等同于在django.conf.urls导入include
from django.conf.urls import url
import xadmin

from users.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', xadmin.site.urls),

    # 验证码路由
    path('captcha/', include('captcha.urls')),

    # 课程机构相关 URL
    path(r'org/', include(('organizations.urls', 'organizations'), namespace='org')),

    # 课程相关 URL 配置
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),

    # 用户中心 URL 配置,看include源码进行配置，默认app_name=None,只有为元组时才能传入参数
    path('users/', include(('users.urls', 'users'), namespace='users')),

]

if settings.DEBUG:
    #  配置静态文件访问处理
    urlpatterns.append(url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))

# 全局页面配置
handler403 = 'users.views.page_not_look'
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
