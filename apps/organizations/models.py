# _*_ coding:utf-8 _*_
from datetime import datetime

from django.db import models


# Create your models here.


class City(models.Model):
    """机构所属城市"""
    name = models.CharField(verbose_name='城市', max_length=20)
    add_time = models.DateField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Organizationinfo(models.Model):
    """授课机构信息"""
    category_choices = (('gx', '高校'), ('pxjg', '培训机构'), ('gr', '个人'))
    category = models.CharField(verbose_name='机构类别', choices=category_choices, default='gx', max_length=20)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name='所在城市')
    name = models.CharField(verbose_name='机构名称', default='', max_length=100)
    image = models.ImageField(verbose_name='机构logo', upload_to='org/%Y/%m', default=100)
    students = models.IntegerField(verbose_name='学习人数', default=0)
    address = models.CharField(verbose_name='机构地址', default='', max_length=200)
    desc = models.TextField(verbose_name='机构介绍', default='')
    add_time = models.DateField(verbose_name='添加时间', default=datetime.now)

    tag = models.CharField(verbose_name='机构标签', default='全国知名', max_length=20)
    click_nums = models.IntegerField(verbose_name='点击数', default=0)
    fav_nums = models.IntegerField(verbose_name='收藏数', default=0)

    # 课程数
    # 经典课程
    # 全部课程
    # 机构教师
    class Meta:
        verbose_name = '授课机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """讲师"""
    org = models.ForeignKey(Organizationinfo, on_delete=models.SET_NULL, null=True, verbose_name='就职公司')
    name = models.CharField(verbose_name='姓名', default='', max_length=20)
    image = models.ImageField(verbose_name='教师头像', upload_to='teacher/%Y/%m',default='teacher/default.png', max_length=100)
    age = models.IntegerField(verbose_name='年龄', default=30)
    work_years = models.IntegerField(verbose_name='工作年限', default=0)
    work_position = models.CharField(verbose_name='工作职位', default='', max_length=20)
    teach_points = models.CharField(verbose_name='教学特点', default='', max_length=50)
    fav_nums = models.IntegerField(verbose_name='收藏数', default=0)
    add_time = models.DateField(verbose_name='添加时间', default=datetime.now)

    click_nums = models.IntegerField(verbose_name='点击数', default=0)

    # 全部课程

    class Meta:
        verbose_name = '讲师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
