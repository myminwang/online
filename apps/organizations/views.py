#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger  # 实现分页功能
from django.http import HttpResponse

from .models import City, Organizationinfo, Teacher
from .forms import UserAskForm
from operation.models import UserAsk, UserFav
from courses.models import Courseinfo


class TeacherListView(View):
    """教师列表"""

    def get(self, request):
        teachers = Teacher.objects.all()
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        keywords = request.GET.get('keywords',)

        # 搜索功能
        if keywords:
            teachers = teachers.filter(name__icontains=keywords)


        # 教师总数
        te_nums = teachers.count()

        # 排序功能
        sort = request.GET.get('sort','')
        if sort == 'hot':
            teachers = teachers.order_by('-click_nums')
            pass

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, 5, request=request)
        teach = p.page(page)

        return render(request, 'teachers-list.html', {
            'teachers': teach,
            'te_nums': te_nums,
            'hot_teachers': hot_teachers,
            'sort': sort,
        })

    pass


class TeacherDetailView(View):
    """教师详情"""

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        te_courses = Courseinfo.objects.filter(teacher_id=teacher_id)

        # 教师点击数
        teacher.click_nums += 1
        teacher.save()

        # 教师排行
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        # 是否已收藏   教师
        is_tea_fav = False
        if request.user.is_authenticated:
            if UserFav.objects.filter(user=request.user, fav_type=2, fav_id=teacher.id):
                is_tea_fav = True

        # 是否已收藏   右侧机构
        is_fav = False
        if request.user.is_authenticated:
            if UserFav.objects.filter(user=request.user, fav_type=1, fav_id=teacher.org.id):
                is_fav = True

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(te_courses, 5, request=request)
        te_course = p.page(page)

        return render(request, 'teacher-detail.html',{
            'teacher': teacher,
            'te_courses': te_course,
            'hot_teachers': hot_teachers,
            'is_tea_fav':is_tea_fav,
            'is_fav':is_fav,
        })


class OrgListView(View):
    """机构列表"""

    def get(self, request):
        """进入机构列表页"""
        all_citys = City.objects.all()
        all_orgs = Organizationinfo.objects.all()
        keywords = request.GET.get('keywords', '')

        # 搜索功能
        if keywords:
            all_orgs = all_orgs.filter(name__icontains=keywords)

        # 右侧授课机构排名
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # 机构类别筛选
        category = request.GET.get('ct', '')
        if category and category != 'None':
            all_orgs = all_orgs.filter(category=category)

        # 城市筛选
        city_id = request.GET.get('city', )
        if city_id and city_id != 'None':
            city_id = int(city_id)
            all_orgs = all_orgs.filter(city_id=city_id)
        if city_id == 'None':
            city_id = ''

        # 筛选后机构的数量
        org_nums = all_orgs.count()

        # 排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'city_id': city_id,
            'all_citys': all_citys,
            'category': category,
            'org_nums': org_nums,
            'all_orgs': orgs,
            'sort': sort,
            'hot_orgs': hot_orgs,
            'keywords': keywords,
        })


class OrgHomeView(View):
    """机构首页，机构详情"""

    def get(self, request, org_id):
        """机构首页显示"""
        org = Organizationinfo.objects.get(id=org_id)
        org_courses = org.courseinfo_set.all()[:4]
        org_teachers = org.teacher_set.all()[:5]

        # 机构点击数
        org.click_nums += 1
        org.save()

        # 判断是否已收藏
        is_fav = False
        if request.user.is_authenticated:
            if UserFav.objects.filter(user=request.user, fav_type=1, fav_id=org_id):
                is_fav = True

        context = {
            'org': org,
            'org_courses': org_courses,
            'org_teachers': org_teachers,
            'is_fav':is_fav,
        }
        return render(request, 'org-detail-homepage.html', context)



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
    """机构教师"""

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

            res['status'] = 'success'
        else:
            res['status'] = 'fail'
            for key, error in userask_form.errors.items():
                res['msg'] = error
                break  # 只显示第一个错误
        return HttpResponse(json.dumps(res), content_type='application/json')


class AddFavView(View):
    """课程机构  用户收藏、取消收藏"""
    def set_fav_nums(self,fav_id,fav_type,sign=1):
        """处理收藏数据"""
        if fav_type == 0:   # 课程收藏
            course = Courseinfo.objects.get(id=fav_id)
            course.fav_nums += sign
            if course.fav_nums < 0:
                course.fav_nums = 0
            course.save()
        if fav_type == 1:   # 机构收藏
            org = Organizationinfo.objects.get(id=fav_id)
            org.fav_nums += sign
            if org.fav_nums < 0:
                org.fav_nums = 0
            org.save()
        if fav_type == 2:   # 教师收藏
            teacher = Teacher.objects.get(id=fav_id)
            teacher.fav_nums += sign
            if teacher.fav_nums < 0:
                teacher.fav_nums = 0
            teacher.save()


    def post(self, request):
        fav_id = request.POST.get('fav_id','')
        fav_type = request.POST.get('fav_type','')

        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        # 是否已收藏
        exist_records = UserFav.objects.filter(user=request.user,fav_id=fav_id,fav_type=fav_type)
        if exist_records:     # 已收藏，点击后取消收藏
            res['status'] = 'success'
            res['msg'] = '收藏'

            self.set_fav_nums(fav_id=fav_id,fav_type=fav_type,sign=-1)
            exist_records.delete()
        else:         # 未收藏，点击收藏
            userfav = UserFav()
            if fav_type and fav_id:
                res['status'] = 'success'
                res['msg'] = '已收藏'

                self.set_fav_nums(fav_id=fav_id, fav_type=fav_type, sign=1)
                userfav.user = request.user
                userfav.fav_id = fav_id
                userfav.fav_type = fav_type
                userfav.save()
            else:
                res['status'] = 'fail'
                res['msg'] = '收藏出错'
        return HttpResponse(json.dumps(res), content_type='application/json')
