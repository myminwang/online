## 在线教育平台  
[![Build Status](https://travis-ci.org/liangliangyy/DjangoBlog.svg?branch=master)](https://travis-ci.org/liangliangyy/DjangoBlog) [![python3.6](https://img.shields.io/badge/python-3.6-brightgreen.svg)]() [![django2.0](https://img.shields.io/badge/django-2.0-brightgreen.svg)]()   
　　该平台的课程由各授课机构提供，授课机构中的各授课老师将录制的视频上传至平台，由平台进行呈现，学员通过平台进行在线学习，<a href="http://www.myminwang.top" target="_blank">项目展示</a>。　　
>项目开发教程及常见问题分析请点击<a href="http://www.zxdt.fun/article/p1/0/" target="_blank">我的博客</a>中均有列出。
    
## 主要功能：  
* 账号注册、激活、登录、密码找回等功能。
* 个人中心页面支持`个人信息`、`我的课程`、`我的收藏`、`我的消息`管理。
* 首页轮播图、机构、课程展示。
* 支持讲师、课程、机构选项的全局搜索。
* 侧边栏提供热门课程推荐、机构/讲师排名、课程咨询。
* 支持授课机构按类别、按地区筛选，按学习人数、课程数排序。

## 环境
* Python 3.6.5
* Django 2.0.6
* MySQL 5.7.22


### 快速启动该项目
1.安装Python 3.6  
2.安装MySQL 5.7 并创建online数据库

    mysql -u root -p
    Enter password: 
    mysql> create database online;
    
3.建立虚拟环境（可省略）

    python3 -m venv venv
    source venv/bin/activate
    
4.项目下载

    git clone https://github.com/myminwang/online.git
    cd online

5.安装Django 2.0

    pip install django
    
6.安装其他依赖包

    pip install -r requirements.txt 
    # 如有个别包不能安装，请下载源码，放到extra_apps里，并在setting里配置
    # pillow包的版本，需要查看官网根据自己的系统选定版本

7.修改配置
```python
# setting.py
# 将数据库密码换成自己的
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'online',
    'USER': 'root',
    'PASSWORD': '1234567',
    'HOST': '127.0.0.1',
    'POST': '3306',
    }
}
```
8.创建数据表

    python manage.py makemigrations
    python manage.py migrate
    
9.运行项目

    python manage.py runserver

在浏览器地址栏输入：127.0.0.1:8000


### 关于Mysql及Navicat安装（ox系统）  

* mysql安装[参考](http://www.cnblogs.com/wendaobiancheng/p/9041278.html)
* Navicat安装，[免费版链接](https://pan.baidu.com/s/1mWqOacmSqWmVD5YgRbUoCg)  密码:sjw4

### 关于项目部署（使用AWS EC2云服务器）  

* 云服务器[申请及配置](https://www.cnblogs.com/wendaobiancheng/p/9172083.html)
* 使用Nginx+uWSGI[部署项目](https://www.cnblogs.com/wendaobiancheng/p/9172425.html)  
