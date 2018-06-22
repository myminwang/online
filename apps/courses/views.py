#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger  # 实现分页功能
from django.db.models import Q

from .models import Courseinfo, Video, Lession
from operation.models import UserCourse, CourseComments, UserFav
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.


class CoursesListView(View):
    """课程列表"""

    def get(self, request):
        all_courses = Courseinfo.objects.all()
        keywords = request.GET.get('keywords', )

        # 热门课程推荐
        hot_courses = Courseinfo.objects.order_by('-click_nums')[:3]

        # 搜索功能,contains相当于like，i表示不区分大小写
        if keywords:
            all_courses = all_courses.filter(name__icontains=keywords)

        # 排序
        sort = request.GET.get('sort', )
        if sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')
        if sort == 'students':
            all_courses = all_courses.order_by('-students')

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 5, request=request)
        allcourses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': allcourses,
            'hot_courses': hot_courses,
            'sort': sort,

        })


class CourseDetailView(View):
    """课程详情"""

    def get(self, request, course_id):
        """课程详情页处理"""
        course = Courseinfo.objects.get(id=course_id)

        # 学习该课程的用户
        users = course.usercourse_set.filter(course_id=course_id)

        # 是否已收藏   课程
        is_course_fav = False
        if request.user.is_authenticated:  # is_authenticated是属性，不是方法
            if UserFav.objects.filter(user=request.user, fav_type=0, fav_id=course_id):
                is_course_fav = True

        # 是否已收藏   右侧机构
        is_fav = False
        if request.user.is_authenticated:  # is_authenticated是属性，不是方法
            if UserFav.objects.filter(user=request.user, fav_type=1, fav_id=course.course_org.id):
                is_fav = True

        return render(request, 'course-detail.html', {
            'course': course,
            'users': users,
            'is_fav':is_fav,
            'is_course_fav':is_course_fav,

        })


class CourseVideoView(LoginRequiredMixin,View):
    """章节/视频列表"""

    def get(self, request, course_id):
        course = Courseinfo.objects.get(id=course_id)
        lessions = course.lession_set.all()
        resources = course.courseresource_set.all()

        # 该课的同学还学过
        # 获取所有学过本课程的用户的id
        user_ids = [usercourse.user_id for usercourse in UserCourse.objects.filter(course_id=course_id)]
        # 获取这些用户学习过的所有课程的id
        user_courses_ids = [usercourse.course_id for usercourse in UserCourse.objects.filter(user_id__in=user_ids)]
        # 对筛选出的课程id进行去重
        usercourses_ids = set(user_courses_ids)
        # 对选出的id对应的课程对象，按照点击数排序后取前3名
        course_lists = Courseinfo.objects.filter(id__in=usercourses_ids).order_by('-click_nums')[:3]

        return render(request, 'course-video.html', {
            'course': course,
            'lessions': lessions,
            'resources': resources,
            'course_lists': course_lists,
        })


class CourseCommentView(View):
    """课程评论"""

    def get(self, request, course_id):
        course = Courseinfo.objects.get(id=course_id)
        resources = course.courseresource_set.all()

        # 该课的同学还学过
        user_ids = [usercourse.user_id for usercourse in UserCourse.objects.filter(course_id=course_id)]
        user_courses_ids = [usercourse.course_id for usercourse in UserCourse.objects.filter(user_id__in=user_ids)]
        usercourses_ids = set(user_courses_ids)
        course_lists = Courseinfo.objects.filter(id__in=usercourses_ids).order_by('-click_nums')[:3]

        # 用户评论
        comments = CourseComments.objects.filter(course_id=course_id).order_by('add_time')[:12]

        return render(request, 'course-comment.html', {
            'course': course,
            'resources': resources,
            'course_lists': course_lists,
            'comments': comments,
        })


class VideoPlayView(View):
    """视频播放页面"""

    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        lession = Lession.objects.get(id=video.lession_id)
        course = Courseinfo.objects.get(id=lession.course_id)
        course_id = course.id
        lessions = course.lession_set.all()
        resources = course.courseresource_set.all()

        user_ids = [usercourse.user_id for usercourse in UserCourse.objects.filter(course_id=course_id)]
        user_courses_ids = [usercourse.course_id for usercourse in UserCourse.objects.filter(user_id__in=user_ids)]
        usercourses_ids = set(user_courses_ids)
        course_lists = Courseinfo.objects.filter(id__in=usercourses_ids).order_by('-click_nums')[:3]

        return render(request, 'course-play.html', {
            'video': video,
            'course': course,
            'lessions': lessions,
            'resources': resources,
            'course_lists': course_lists,

        })
