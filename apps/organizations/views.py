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
    pass


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
    """机构首页"""

    def get(self, org_id):
        """"""
        pass


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
            return HttpResponse(res, content_type='application/json')
        else:
            res['status'] = 'fail'
            res['msg'] = '添加出错'
        return HttpResponse(res.__format__(userask_form.errors), content_type='application/json')
