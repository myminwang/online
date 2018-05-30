# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password  # 对明文进行加密模块

from .forms import RegisterForm
from .models import UserProfile
from utils.email_send import send_link_email
# Create your views here.


class RegisterView(View):
    """用户注册功能"""

    def get(self, request):
        """get方法获取URL中数据"""
        # 不允许get方式注册
        return render(request, 'register.html', {})

    def post(self, request):
        """
        获取html传回的form数据
        form验证，数据库存在验证
        保存到数据库
        """
        # 进行form验证
        register_form = RegisterForm(request.POST)  # 将html提供的POST对象传入,并将判断结果传回给变量
        if register_form.is_valid():  # is_valid()为固定用法，判断是否验证通过

            # 验证通过，获取用户输入的参数
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            if UserProfile.objects.filter(email=email):  # 判断邮箱是否已经注册过了
                # 如果使用get方法，未匹配到会报错，使用filter未匹配到返回[]，为False
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在！'})
            else:
                user_profile = UserProfile()
                user_profile.username = email
                user_profile.email = email
                user_profile.password = make_password(password)
                user_profile.is_active = False
                user_profile.save()

                send_link_email(email)  # 发送激活邮件
                return render(request, "email_send_success.html", {'email': email, 'msg': '请前往查收并尽快激活账户'})

        else:
            return render(request, 'register.html', {'register_form': register_form})


class LoginView(View):
    """用户登录功能"""

    def get(self, request):
        return render(request, 'login.html', {})
