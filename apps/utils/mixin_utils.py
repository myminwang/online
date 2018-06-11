#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "2018-06-11 18:46"

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """验证用户是否登录，如未登录转到登录页面"""
    @method_decorator(login_required(login_url='/users/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
