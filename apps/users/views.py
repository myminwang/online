# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password  # 对明文进行加密模块
from django.http import HttpResponse
from django.contrib.auth import login  # 登录模块
from django.db.models import Q  # or功能

from .forms import RegisterForm, LoginForm
from .models import UserProfile, EmailVerification
from utils.email_send import send_link_email


# Create your views here.


class IndexView(View):
    """显示首页"""

    def get(self, request):
        return render(request, 'index.html', {})


class RegisterView(View):
    """用户注册功能"""

    def get(self, request):
        """get方法获取URL中数据,调用验证码模块，render到网页中，否则不显示验证码"""
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        """
        获取html传回的form数据
        form验证、数据库存在验证
        发送验证邮件、保存到数据库
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

                try:
                    send_link_email(email)  # 发送激活邮件
                except AttributeError:
                    return render(request, 'register.html', {'msg': '邮箱错误'})
                return render(request, "email_send_success.html", {'email': email, 'msg': '请前往查收并尽快激活账户'})

        else:
            return render(request, 'register.html', {'register_form': register_form})


class RegisterActiveView(View):
    """注册激活功能"""

    def get(self, request, active_code):
        """获取url中的验证码"""
        regis_actives = EmailVerification.objects.filter(code=active_code, is_delete=0)
        # 如果在数据库中有符合要求的数据，则返回该对象（包括数据库中该行记录）给regis_actives
        if regis_actives:
            for regis_active in regis_actives:  # 第一次遍历，regis_active获取该对象在数据库中的该行记录，类字典方式存在变量中
                email = regis_active.email
                user = UserProfile.objects.get(email=email)  # 获取用户信息中此邮箱的用户，将该条记录以类字典方式传给user
                user.is_active = True
                user.save()

                regis_active.is_delete = 1
                regis_active.save()
                return render(request, 'login.html', {})
        else:
            return render(request, 'register_active_failed.html', {})


class LoginView(View):
    """用户登录功能"""

    def get(self, request):
        """不允许get方式登录"""
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_user = request.POST.get('username', '')
            login_password = request.POST.get('password', '')

            # 使用django自带的身份验证模块
            try:
                user = UserProfile.objects.get(Q(username=login_user) | Q(email=login_user))
                if not user.is_active:
                    return render(request, 'login.html', {'msg': '用户未激活'})
                elif user.check_password(login_password):
                    login(request, user)
                    return render(request, 'index.html', {})
            except Exception as e:
                return None
        else:
            return render(request, 'login.html', {'login_form': login_form})
