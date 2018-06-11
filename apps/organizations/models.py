# _*_ coding:utf-8 _*_
from datetime import datetime

from django.db import models


# Create your models here.


class City(models.Model):
    """机构所属城市"""
    name = models.CharField(verbose_name='城市', max_length=20)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Organizationinfo(models.Model):
    """授课机构信息"""
    category_choices = (('gx', '高校'), ('pxjg', '培训机构'), ('gr', '个人'))
    category = models.CharField(verbose_name='机构类别', choices=category_choices, default='gx', max_length=20)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='所在城市')
    name = models.CharField(verbose_name='机构名称', default='', max_length=100)
    image = models.ImageField(verbose_name='机构logo', upload_to='orgs/%Y/%m', max_length=100)
    students = models.IntegerField(verbose_name='学习人数', default=0)
    address = models.CharField(verbose_name='机构地址', default='', max_length=200)
    desc = models.TextField(verbose_name='机构介绍', default='')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)
    is_authentication = models.BooleanField(verbose_name='是否已认证', choices=((0, '未认证'), (1, '已认证')), default=0)
    is_gold = models.BooleanField(verbose_name='是否为金牌机构', choices=((0, '非金牌机构'), (1, '金牌机构')), default=0)
    # 金牌机构必须是已获得认证的
    course_nums = models.IntegerField(verbose_name='课程数', default=0)

    tag = models.CharField(verbose_name='机构标签', default='全国知名', max_length=20)
    click_nums = models.IntegerField(verbose_name='点击数', default=0)
    fav_nums = models.IntegerField(verbose_name='收藏数', default=0)

    # 经典课程
    # 机构教师
    def teacher_nums(self):
        """获取该机构的教师数量"""
        return self.teacher_set.count()
    teacher_nums.short_description = '教师人数'

    # def get_course_nums(self):
    #     """获取该机构课程总数"""
    #     course_nums = self.courseinfo_set.all().count()
    #     self.save()
    #     return course_nums
    # get_course_nums.short_description = '课程总数'

    class Meta:
        verbose_name = '授课机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """教师"""
    org = models.ForeignKey(Organizationinfo, on_delete=models.CASCADE, verbose_name='就职单位')
    name = models.CharField(verbose_name='姓名', default='', max_length=20)
    image = models.ImageField(verbose_name='头像', upload_to='teachers/%Y/%m', default='default1.png', max_length=100)
    age = models.IntegerField(verbose_name='年龄', default=30)
    work_years = models.IntegerField(verbose_name='工作年限', default=0)
    work_position = models.CharField(verbose_name='工作职位', default='', max_length=20)
    teach_points = models.CharField(verbose_name='教学特点', default='', max_length=50)
    fav_nums = models.IntegerField(verbose_name='收藏数', default=0)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)
    is_authentication = models.BooleanField(verbose_name='是否已认证', choices=((0, '未认证'), (1, '已认证')), default=0)
    is_gold = models.BooleanField(verbose_name='是否为金牌教师', choices=((0, '非金牌教师'), (1, '金牌教师')), default=0)
    # 金牌教师必须是已获得认证的

    click_nums = models.IntegerField(verbose_name='点击数', default=0)

    def course_nums(self):
        """课程数量"""
        return self.courseinfo_set.count()  # 使用'实例.course_nums()'调用该方法获取值，在前端可以使用'实例.course_nums'直接获取值
    course_nums.short_description = '课程数量'

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
