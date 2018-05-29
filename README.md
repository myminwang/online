# 在线教育平台
###   该平台的课程由各授课机构提供，授课机构中的各授课老师将录制的视频上传至平台，由平台进行呈现，学员通过平台进行在线学习，[项目展示](http://52.193.67.154)。
本项目在开发及调试过程中遇到的问题，我会在个人博客进行发布,[我的博客](http://www.cnblogs.com/wendaobiancheng/ "欢迎关注")。
## 一、网页结构及功能实现：
* **首页**：首页名称、logo展示、登录/注册/个人中心入口、内容搜索、下拉功能菜单、轮播图、公开课展示、机构展示、页脚；

* **课程页面**（首页->公开课）：公开课列表，右侧过滤热门公开课的推荐，可对课程进行分页；
  * 课程详情页（首页->公开课->课程）：展示课程详情（由后台富文本编辑生成），可对课程进行收藏、开始学习，右侧为课程机构的简单介绍；
  * 课程学习页（首页->公开课->课程->开始学习）：展示课程章节信息，点击章节跳转到响应的播放页面，即可开始该章内容的学习，并可对该课程进行评论，右侧为该课程课程资料的下载展示；

* **讲师页面**（首页->授课讲师）：授课讲师列表页，可按人气进行排序，可对内容进行分页，右侧展示讲师排行榜；
  * 讲师详情页（首页->授课讲师->讲师）：展示讲师简介，在授课程等；

* **授课机构页面**（首页->授课机构）：授课机构列表，可按类别、地区进行筛选，可按学习人数、评论数进行排序，右侧上方为用户提交我要学习的咨询窗口，下方为机构的排名；
  * 授课机构详情页（首页->授课机构->机构）：该授课机构首页，可点击进行收藏，可分别进入机构课程、机构介绍、机构讲师等页面；

* **个人中心页面**（首页->个人中心）：用户注册、登录、邮箱激活验证、密码找回、个人信息展示、修改页面，同时可分别进入我的课程、我的收藏、我的消息等页面；


## 二、环境搭建及包的安装
* 系统为OX10.11.6，如果使用其他系统，在安装pillow时，需要安装官网显示的适配版本
* python版本为3.6.5
* pip install virtualenv
* virtualenv venv
* source venv/bin/activate
* cd online
使用以下命令安装：
* pip install -r requirements.txt


## 三、APPS设计
* users - 用户管理；
* courses - 课程管理；
* organization - 机构和教师管理；
* operation - 用户操作管理（设计目的：如用户models中的课程会引用课程models的数据，而课程models中的评论又会引用用户models中的数据造成的
循环引用的情况，但是Django不允许循环引用的存在，所以要进行分层设计，operation为顶层APP，可以引用下一层APP，防止下一层的models循环引用）；


## 四、models设计
* users models：
    * UserProfile - 用户基本信息；
    * EmailVerifyRecord - 邮箱验证；
    * Banner - 轮播图；
        说明：邮箱验证和轮播图都是单独的模块，放到该APP一起处理；
* courses models：
    * Course - 课程基本信息；
    * Lesson - 章节信息；
    * Video - 视频；
    * CourseResource - 课程资源；
        说明：共有三层结构，课程-章节-视频；课程表（同视频是一对多的关系，同章节是一对多的关系）、章节表（同视频也是一对多关系），视频资源表，课程资源表（页面右侧的资料下载），共四张表；
* organization models:
    * CourseOrg - 课程机构基本信息；
    * Teacher - 教师基本信息；
    * CityDict - 城市信息；
        说明：包含课程类别、课程所在地（动态）、机构列表、我要学习窗口等；
* operation models:
    * UserAsk - 用户咨询；
    * CourseComments - 用户评论；
    * UserFavorite - 用户收藏；
    * UserMessage - 用户消息；
    * UserCourse - 用户学习的课程；
        说明：在授课机构右侧上方的提交窗口需要一张表来存储、课程评论表、收藏（课程、讲师、机构）表、消息表、用户与课程之间的关系表


## 五、后台管理系统-Xadmin
* 不建议直接使用pip install xadmin，可能会由于django的不匹配而重新安装低版本的django
        安装方法：
        pip install git+git://github.com/sshwsfc/xadmin.git@django2
    * 安装完成后需要修改配置文件setting.py，在APPS中添加xadmin和crispy_forms；
    * 使用xadmin时需要在每个APP目录下新建adminx.py文件；  
    
        import xadmin  
        from .models import *  
        class 模块Admin(object):  
        xadmin.site.register(模块,模块Admin)  
        
    * 进行页面头部名称、底部名称修改时，只需要修改其中的一个APP下的adminx.py文件即可，请注意引用的模块及注册的方式（本项目修改的文件为apps/users/adminx.py）；
    * 对页面左侧模型名称修改为中文，同django自带的admin下的修改一致：
        每个APP文件下的apps.py文件修改为（以uses为例）：  
        
        from django.apps import AppConfig  
        class UsersConfig(AppConfig):  
            name = 'users'  
            verbose_name = u'用户信息'  
            
        每个APP文件下的__init__.py文件添加（以uses为例）：  
        
        default_app_config = "users.apps.UsersConfig"

## 六、文件目录结构：
* Online_learning    项目根目录  
* |-- apps           自建apps  
* |   |-- courses  
* |   |-- operation  
* |   |-- organization  
* |   |-- users  
* |   `-- utils  
* |-- extra_apps     第三方包  
* |   `-- xadmin  
* |-- imooc         项目名称  
* |-- LICENSE  
* |-- manage.py  
* |-- media         接收文件目录  
* |   |-- banner  
* |   |-- courses  
* |   |-- org  
* |   `-- teacher  
* |-- README.md  
* |-- requirements.txt  
* |-- static          静态文件目录  
* |   |-- admin  
* |   |-- css  
* |   |-- images  
* |   |-- img  
* |   |-- js  
* |   |-- media  
* |   `-- xadmin  
* |-- templates       网页文件目录  
* `-- uwsgi_params  
## 七、Mysql及Navicat安装（ox系统）
* mysql安装请参考[http://www.cnblogs.com/wendaobiancheng/p/9041278.html](http://www.cnblogs.com/wendaobiancheng/p/9041278.html)
* Navicat安装，mac免费版链接：https://pan.baidu.com/s/1mWqOacmSqWmVD5YgRbUoCg  密码:sjw4

## 待解决问题：
* xadmin，后台管理不能显示APP的中文名称
        每个APP文件下的__init__.py文件添加（以uses为例）：

        default_app_config = "users.apps.UsersConfig"

        使用runserver或makemigrations时，报错：
        ModuleNotFoundError: No module named 'users'
