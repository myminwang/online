#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger # 实现分页功能

from .models import City, Organizationinfo


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
        hot_orgs = all_orgs.order_by('-course_nums')[:3]

        # 机构类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

            # 城市筛选
            city_id = request.GET.get('city', )
        if city_id:
            all_orgs = all_orgs.filter(city=city_id)

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
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)


        return render(request, 'org-list.html', {
            'city_id': city_id,
            'all_citys': all_citys,
            'category': category,
            'org_nums': org_nums,
            'all_orgs': all_orgs,
            'sort': sort,
            'hot_orgs': hot_orgs, })

    pass


class OrgHomeView(View):
    """机构首页"""

    def get(self, org_id):
        """"""
        pass
