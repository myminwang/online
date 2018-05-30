# _*_ coding:utf-8 _*_
from datetime import datetime

from django.db import models

# Create your models here.

from organizations.models import Organizationinfo, Teacher


class Courseinfo(models.Model):
    """课程信息"""
    course_org = models.ForeignKey(Organizationinfo, on_delete=models.CASCADE, null=True, verbose_name='所属机构')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, verbose_name='讲师')
    name = models.CharField(max_length=100, verbose_name='课程名称')
    image = models.ImageField(verbose_name='课程封面', upload_to='courses/%Y/%m', max_length=100)
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    degree_choice = (('cj', '初级'), ('zj', '中级'), ('gj', '高级'))
    degree = models.CharField(verbose_name='难度',
                              choices=degree_choice, default='cj', max_length=2)
    students = models.IntegerField(verbose_name='学习人数', default=0)
    learn_time = models.IntegerField(verbose_name='学习时长（分钟数）', default=0)
    category = models.CharField(verbose_name='课程类别',
                                default='后端', max_length=100)
    fav_nums = models.IntegerField(verbose_name='收藏人数', default=0)
    click_nums = models.IntegerField(verbose_name='点击数', default=0)
    detail = models.TextField(verbose_name='课程详情')
    is_banner = models.BooleanField(verbose_name='是否为轮播图', default=False)
    before_know = models.CharField(verbose_name='课前须知', max_length=300, default='')
    teacher_tell = models.CharField(verbose_name='老师告诉你能学到什么', max_length=300, default='')
    add_time = models.DateField(verbose_name='添加时间', default=datetime.now)

    # 章节数
    # 学习用户展示
    # 课程标签
    # 课程评论

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseBanner(Courseinfo):
    """
    课程轮播图
    在首页展示的
    继承课程信息
    """
    # 暂时不知此模块作用！！！
    # 播放次序
    # 链接
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name


class Lession(models.Model):
    """
    章节信息
    点击我要学习进入
    """
    course = models.ForeignKey(Courseinfo, on_delete=models.CASCADE, null=True, verbose_name='课程')
    name = models.CharField(verbose_name='章节名', max_length=100)
    add_time = models.DateField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    """视频信息"""
    # 外键至章节
    # 播放地址
    # 添加时间
    lession = models.ForeignKey(Lession, on_delete=models.CASCADE, null=True, verbose_name='章节')
    name = models.CharField(verbose_name='视频名称', max_length=100)
    url = models.URLField(verbose_name='播放地址', max_length=200, default='https://v.youku.com/v_show/id_XMzU3ODg1MjUwMA'
                                                                       '.html?spm=a2hww.20027244.m_250379.5~1~3!2~A')
    learn_time = models.IntegerField(verbose_name='视频时长（分钟数）', default=0)
    add_time = models.DateField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    """资料下载,如课件等资料"""
    # 资料名称
    # 下载地址
    # 添加时间
    lession = models.ForeignKey(Courseinfo, on_delete=models.CASCADE, null=True, verbose_name='课程')
    name = models.CharField(verbose_name='资料名称', max_length=100)
    download = models.FileField(verbose_name='资料下载', upload_to='course/resource/%Y/%m', max_length=100)
    add_time = models.DateField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
