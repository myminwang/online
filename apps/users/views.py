# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.


class RegisterView(View):
    """用户注册功能"""
    def get(self, request):
        return render(request,'register.html',{})
