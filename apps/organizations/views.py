#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger  # 实现分页功能
from django.http import HttpResponse

from .models import City, Organizationinfo
from .forms import UserAskForm
from operation.models import UserAsk


# Create your views here.


class TeacherListView(View):
    """讲师列表"""

    def get(self, request):
        return render(request, 'teachers-list.html')

    pass


class TeacherDetailView(View):
    """讲师详情"""

    def get(self, request, teacher_id):
        return render(request, 'teacher-detail.html')


class OrgListView(View):
    """机构列表"""

    def get(self, request):
        """进入机构列表页"""
        all_citys = City.objects.all()
        all_orgs = Organizationinfo.objects.all()

        # 右侧授课机构排名（根据拥有的课程数排名，取前3名），不能放到后面，下面的all_org会改变
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # 机构类别筛选
        category = request.GET.get('ct', '')
        if category and category != 'None':
            all_orgs = all_orgs.filter(category=category)

        # 城市筛选
        city_id = request.GET.get('city', )
        if city_id and city_id != 'None':
            org_city_id = City.objects.get(name=city_id)
            all_orgs = all_orgs.filter(city_id=org_city_id.id)

        # 筛选后机构的数量
        org_nums = all_orgs.count()

        # 排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        # 分页功能
        # 尝试获取前台get请求传递过来的page参数
        # # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)  # 这里指从allorg中取五个出来，每页显示5个
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'city_id': city_id,
            'all_citys': all_citys,
            'category': category,
            'org_nums': org_nums,
            'all_orgs': orgs,
            'sort': sort,
            'hot_orgs': hot_orgs, })


class OrgHomeView(View):
    """机构首页，机构详情"""

    def get(self, request, org_id):
        """机构首页显示"""
        org = Organizationinfo.objects.get(id=org_id)
        org_courses = org.courseinfo_set.all()[:4]
        org_teachers = org.teacher_set.all()[:5]
        context = {
            'org': org,
            'org_courses': org_courses,
            'org_teachers': org_teachers,
        }
        return render(request, 'org-detail-homepage.html', context)


# 机构推荐指数
# 收藏机构

class OrgCourseView(View):
    """机构课程"""

    def get(self, request, org_id):
        org = Organizationinfo.objects.get(id=org_id)
        org_courses = org.courseinfo_set.all()

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(org_courses, 8, request=request)
        orgcourses = p.page(page)

        context = {
            'org': org,
            'org_courses': orgcourses,
        }
        return render(request, 'org-detail-course.html', context)


class OrgTeacherListView(View):
    """机构讲师"""

    def get(self, request, org_id):
        org = Organizationinfo.objects.get(id=org_id)
        org_teachers = org.teacher_set.all()

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(org_teachers, 5, request=request)
        orgteachers = p.page(page)

        return render(request, 'org-detail-teachers.html', {
            'org': org,
            'org_teachers': orgteachers,
        })


class OrgDescView(View):
    """机构介绍"""

    def get(self, request, org_id):
        org = Organizationinfo.objects.get(id=org_id)
        return render(request, 'org-detail-desc.html', {'org': org})


class UserAskView(View):
    """用户咨询处理"""

    # 比较合理的操作是异步的，不会对整个页面进行刷新。如果有错误，显示错误。一种ajax的异步操作。
    # 因此我们此时不能直接render一个页面回来。应该是给前端返回json数据，而不是页面
    # HttpResponse类指明给用户返回哪种类型数据
    def post(self, request):
        """用户咨询"""
        userask = UserAsk()
        userask_form = UserAskForm(request.POST)
        res = dict()
        if userask_form.is_valid():
            userask.name = request.POST.get('name', '')
            userask.mobile = request.POST.get('mobile', '')
            userask.course_name = request.POST.get('course_name', '')
            userask.save()
            # userask_form.save(commit=True)

            res['status'] = 'success'
        else:
            res['status'] = 'fail'
            for key, error in userask_form.errors.items():
                res['msg'] = error
                break  # 只显示一个错误
        return HttpResponse(json.dumps(res), content_type='application/json')
