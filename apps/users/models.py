# _*_ coding:utf-8 _*_
import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    """
    用户基本信息,
    继承AbstractUser类，需要在setting里配置AUTH_USER_MODEL
    """
    nick_name = models.CharField(max_length=20, verbose_name='昵称', default='')
    birthday = models.DateField(verbose_name='生日', null=True)
    gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女')), default='male',
                              verbose_name='性别')
    address = models.CharField(max_length=100, default='', verbose_name='地址')
    mobile = models.IntegerField(verbose_name='手机号', null=True)
    image = models.ImageField(verbose_name='用户头像', upload_to='image/%Y/%m', default='image?default.png')
    add_time = models.DateField(verbose_name='添加时间', default=datetime.datetime.now)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        # 在python 2.7 使用__unicode__(self)
        return self.username


class EmailVerification(models.Model):
    """邮箱验证相关"""
    email = models.EmailField(max_length=50, null=True, verbose_name='邮箱')
    code = models.CharField(max_length=50, verbose_name='验证信息')
    send_type = models.CharField(max_length=20, verbose_name='验证码类型',
                                 choices=(('register', '注册'), ('forget', '修改密码'), ('update_email', '修改邮箱')),
                                 default='register')
    send_time = models.DateField(verbose_name='添加时间', default=datetime.datetime.now)

    class Meta:
        verbose_name = '邮箱验证信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email


class Banner(models.Model):
    """轮播图管理"""
    image = models.ImageField(verbose_name='轮播图', upload_to='image/%Y/%m', max_length=200)
    banner_url = models.URLField(verbose_name='轮播图链接', max_length=100)
    order = models.IntegerField(default=100, verbose_name='顺序')

    class Meta:
        verbose_name = '轮播图管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.image
