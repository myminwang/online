# _*_ coding:utf-8 _*_
import json

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password  # 对明文进行加密模块
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout  # 登录模块、用户验证方法
from django.contrib.auth.backends import ModelBackend  # 包含authenticate方法的模块，进行重写，需要在setting里配置
from django.db.models import Q  # or功能
from pure_pagination import Paginator, PageNotAnInteger  # 实现分页功能

from .forms import RegisterForm, LoginForm, ForgetpwdForm, PwdmodifyForm, UpImageForm, UpUserInfoForm
from .models import UserProfile, EmailVerification, Banner
from utils.email_send import send_link_email
from operation.models import UserCourse, UserFav, UserMessage
from organizations.models import Organizationinfo, Teacher
from courses.models import Courseinfo
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.


class IndexView(View):
    """显示首页"""

    def get(self, request):
        banners = Banner.objects.all().order_by('-order')[:3]
        courses = Courseinfo.objects.all().order_by('-click_nums')[:6]
        orgs = Organizationinfo.objects.all().order_by('click_nums').order_by('-course_nums')[:15]
        banner_courses = Courseinfo.objects.filter(is_banner=True).order_by('-click_nums')[:3]

        return render(request, 'index.html', {
            'banners': banners,
            'courses': courses,
            'orgs': orgs,
            'banner_courses':banner_courses,
        })


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

    def get(self, request, url_active_code):
        """获取url中的验证码"""
        regis_actives = EmailVerification.objects.filter(code=url_active_code, is_delete=0)
        # 如果在数据库中有符合要求的数据，则返回该对象（包括数据库中该行记录）给regis_actives
        if regis_actives:
            for regis_active in regis_actives:  # 第一次遍历，regis_active获取该对象在数据库中的该行记录，类字典方式存在变量中
                email = regis_active.email
                user = UserProfile.objects.get(email=email)  # 获取用户信息中此邮箱的用户，将该条记录以类字典方式传给user
                user.is_active = True
                user.save()

                regis_active.is_delete = 1
                regis_active.save()
                return render(request, 'register_active_sucessed.html', {})
        else:
            return render(request, 'register_active_failed.html', {})


class ChongxieAuthenticate(ModelBackend):
    """重写authenticate方法,使之可以对邮箱验证"""

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            return None


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

            # 使用django自带的用户名、密码验证
            user = authenticate(username=login_user, password=login_password)
            if user:  # 通过验证
                if user.is_active:  # 已激活
                    login(request, user)
                    return render(request, 'index.html', {})
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'login_form': login_form, 'msg': '用户名或密码错误'})

            # 验证用户名、密码、是否激活
            # try:
            #     users = UserProfile.objects.get(Q(username=login_user) | Q(email=login_user))
            #     if not users.is_active:
            #         return render(request, 'login.html', {'msg': '用户未激活'})
            #     elif users.check_password(login_password):  # django自带的转密文的密码验证方式
            #         login(request, users)
            #         return render(request, 'index.html', {})
            #     else:
            #         return render(request, 'login.html', {'login_form': login_form, 'msg': '用户名或密码错误'})
            # except Exception as e:
            #     return render(request, 'login.html', {'login_form': login_form, 'msg': '用户未注册'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class ForgetpwdView(View):
    """忘记密码功能"""

    def get(self, request):
        """get方法获取URL中数据,调用验证码模块，render到网页中，否则不显示验证码"""
        forgetpwd_form = ForgetpwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})

    def post(self, request):
        """获取邮箱并发送重置密码链接"""
        forgetpwd_form = ForgetpwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                try:
                    send_link_email(email, send_type='forget')  # 发送重置密码链接
                except AttributeError:
                    return render(request, 'forgetpwd.html', {'msg': '邮箱错误'})
                return render(request, "email_send_success.html", {'email': email, 'msg': '请前往查收并点击链接重置密码'})
            else:
                return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form, 'msg': '该邮箱未注册'})
        else:
            return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})


class PwdresetView(View):
    """密码重置链接处理"""

    def get(self, request, url_pwdreset_code):
        pwdreset_code = url_pwdreset_code
        users = EmailVerification.objects.filter(code=pwdreset_code, is_delete=0)
        if users:
            for user in users:
                email = user.email
                return render(request, 'password_reset.html', {'email': email, 'pwdreset_code': pwdreset_code})
        else:
            return render(request, 'register_active_failed.html')


class PwdmodifyView(View):
    """密码重置功能"""

    def post(self, request):
        """密码重置处理"""
        pwdmodify_form = PwdmodifyForm(request.POST)
        if pwdmodify_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            pwdmodify_email = request.POST.get('email', '')
            pwdmodify_code = request.POST.get('pwdreset_code', '')
            if password1 == password2:
                pwdmodify_user = UserProfile.objects.get(email=pwdmodify_email)
                pwdmodify_user.password = make_password(password1)
                pwdmodify_user.save()  # 更新数据库中的密码

                pwdmodify_code_e = EmailVerification.objects.get(code=pwdmodify_code)
                pwdmodify_code_e.is_delete = 1
                pwdmodify_code_e.save()

                return render(request, 'login.html', {'pwdreset_msg': '密码重置成功，请登录'})
            else:
                return render(request, 'password_reset.html',
                              {'pwdmodify_form': pwdmodify_form, 'msg': '两次输入不一致，请重新输入'})
        else:
            return render(request, 'password_reset.html', {'pwdmodify_form': pwdmodify_form})


class LogoutView(View):
    """注销登录功能"""

    def get(self, request):
        """get方式进行注销登录"""
        logout(request)  # 源码显示，logout只需要一个参数
        return render(request, 'index.html')


class UserInfoView(View):
    """用户的个人中心"""

    def get(self, request):
        """进入个人中心"""
        user = request.user.username
        if not user:  # 未登录
            return render(request, 'login.html', {'pwdreset_msg': '您还未登录...'})
        else:

            return render(request, 'usercenter-info.html')


class MyCourseView(View):
    """个人中心之我的课程"""

    def get(self, request):
        user_id = request.user.id
        courses = UserCourse.objects.filter(user_id=user_id)
        return render(request, 'usercenter-mycourse.html', {
            'courses': courses,
        })


class MyfavCourseView(View):
    """个人中心之我收藏的课程"""

    def get(self, request):
        user_id = request.user.id
        fav_ids = [userfav.fav_id for userfav in UserFav.objects.filter(user_id=user_id, fav_type=0)]
        courses = Courseinfo.objects.filter(id__in=fav_ids)
        return render(request, 'usercenter-fav-course.html', {
            'courses': courses,

        })


class MyfavOrgView(View):
    """个人中心之我收藏的机构"""

    def get(self, request):
        user_id = request.user.id
        fav_ids = [userfav.fav_id for userfav in UserFav.objects.filter(user_id=user_id, fav_type=1)]
        orgs = Organizationinfo.objects.filter(id__in=fav_ids)
        return render(request, 'usercenter-fav-org.html', {
            'orgs': orgs,

        })


class MyfavTeacherView(View):
    """个人中心之我收藏的教师"""

    def get(self, request):
        user_id = request.user.id
        fav_ids = [userfav.fav_id for userfav in UserFav.objects.filter(user_id=user_id, fav_type=2)]
        teachers = Teacher.objects.filter(id__in=fav_ids)
        return render(request, 'usercenter-fav-teacher.html', {
            'teachers': teachers,
        })


class MyMessageView(View):
    """个人中心之我的消息"""

    def get(self, request):
        user_id = request.user.id
        messages = UserMessage.objects.filter(Q(user_id=user_id) | Q(user_id=0))

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(messages, 5, request=request)
        messagess = p.page(page)

        return render(request, 'usercenter-message.html', {
            'messages': messagess,
        })


class UploadImageView(LoginRequiredMixin, View):
    """个人中心头像修改"""

    def post(self, request):
        uploadimage_forms = UpImageForm(request.POST, request.FILES, instance=request.user)
        res = dict()
        if uploadimage_forms.is_valid():
            uploadimage_forms.save()
            res['status'] = 'success'
            res['msg'] = '头像修改成功'
        else:
            res['status'] = 'fail'
            res['msg'] = '头像修改失败'
        return HttpResponse(json.dumps(res), content_type='application/json')


class UploadPwdView(LoginRequiredMixin, View):
    """个人中心的密码修改"""

    def post(self, request):
        pwdmodify_form = PwdmodifyForm(request.POST)
        res = dict()
        if pwdmodify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                res['status'] = 'fail'
                res['msg'] = '两次密码不一致'
                return HttpResponse(json.dumps(res), content_type='application/json')

            user = request.user
            user.password = make_password(pwd2)
            user.save()

            res['status'] = 'success'
            res['msg'] = '密码修改成功'
        else:
            res = pwdmodify_form.errors
        return HttpResponse(json.dumps(res), content_type='application/json')


class UploadUserInfoView(LoginRequiredMixin, View):
    """个人中心的个人资料修改"""

    def post(self, request):
        user_form = UpUserInfoForm(request.POST, instance=request.user)
        res = dict()
        if user_form.is_valid():
            user = UserProfile.objects.get(id=request.user.id)
            user.nick_name = request.POST.get('nick_name', '')
            user.birthday = request.POST.get('birthday', '')
            user.gender = request.POST.get('gender', '')
            user.address = request.POST.get('address', '')
            user.mobile = request.POST.get('mobile', '')
            user.save()

            res['status'] = 'success'
        else:
            res = user_form.errors
        return HttpResponse(json.dumps(res), content_type='application/json')
