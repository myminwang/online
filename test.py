#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "2018-06-04 16:59"

def application(venv, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "Hello World from uWSGI"