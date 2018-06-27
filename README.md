## 在线教育平台  
该平台的课程由各授课机构提供，授课机构中的各授课老师将录制的视频上传至平台，由平台进行呈现，学员通过平台进行在线学习，[项目展示](http://www.myminwang.top)。
>本项目在开发及调试过程中遇到的问题，在[我的博客](http://www.cnblogs.com/wendaobiancheng/ "欢迎关注")中均有列出。
### 网页结构及功能：
* **首页**：`平台名称`、`logo展示`、`登录/注册/个人中心入口`、`内容搜索`、`功能菜单`、`轮播图`、`公开课展示`、`机构展示`、`页脚`；

* **课程页面**（首页->公开课）：`公开课列表`、`热门公开课`；
>课程详情页（首页->公开课->课程）：展示课程详情（由后台富文本编辑生成），可对课程进行收藏、开始学习，右侧为课程机构的简单介绍；  
>课程学习页（首页->公开课->课程->开始学习）：展示课程章节信息，点击章节跳转到响应的播放页面，即可开始该章内容的学习，并可对该课程进行评论，右侧为该课程课程资料的下载展示；

* **教师页面**（首页->授课教师）：`授课教师列表`，可按人气进行排序，可对内容进行分页，右侧展示`教师排行榜`；
>教师详情页（首页->授课教师->教师）：展示教师简介，在授课程等；

* **授课机构页面**（首页->授课机构）：`授课机构列表`，可按类别、地区进行筛选，可按学习人数、评论数进行排序，右侧上方为用户提交我要学习的`咨询窗口`，下方为`机构排名`；
>授课机构详情页（首页->授课机构->机构）：该授课机构首页，可点击进行收藏，可分别进入机构课程、机构介绍、机构教师等页面；

* **个人中心页面**（首页->个人中心）：`用户注册`、`登录`、`邮箱激活验证`、`密码找回`、`个人信息`展示/修改，同时可分别进入`我的课程`、`我的收藏`、`我的消息`等页面；


### 环境
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


### Mysql及Navicat安装（ox系统）
* mysql安装请[参考](http://www.cnblogs.com/wendaobiancheng/p/9041278.html)
* Navicat安装，mac[免费版链接](https://pan.baidu.com/s/1mWqOacmSqWmVD5YgRbUoCg)  密码:sjw4

### 项目部署（使用AWS EC2云服务器）
* 云服务器[申请及配置](https://www.cnblogs.com/wendaobiancheng/p/9172083.html)
* 使用Nginx+uWSGI[部署项目](https://www.cnblogs.com/wendaobiancheng/p/9172425.html)
