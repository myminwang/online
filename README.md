# 在线教育平台
###   该平台的课程由各授课机构提供，授课机构中的各授课老师将录制的视频上传至平台，由平台进行呈现，学员通过平台进行在线学习，[项目展示](http://52.193.67.154)。
本项目在开发及调试过程中遇到的问题，我会在个人博客进行发布,[我的博客](http://www.cnblogs.com/wendaobiancheng/ "欢迎关注")。
## 一、网页结构及功能实现：
* **首页**：首页名称、logo展示、登录/注册/个人中心入口、内容搜索、下拉功能菜单、轮播图、公开课展示、机构展示、页脚；

* **课程页面**（首页->公开课）：公开课列表，右侧过滤热门公开课的推荐，可对课程进行分页；
  * 课程详情页（首页->公开课->课程）：展示课程详情（由后台富文本编辑生成），可对课程进行收藏、开始学习，右侧为课程机构的简单介绍；
  * 课程学习页（首页->公开课->课程->开始学习）：展示课程章节信息，点击章节跳转到响应的播放页面，即可开始该章内容的学习，并可对该课程进行评论，右侧为该课程课程资料的下载展示；

* **教师页面**（首页->授课教师）：授课教师列表页，可按人气进行排序，可对内容进行分页，右侧展示教师排行榜；
  * 教师详情页（首页->授课教师->教师）：展示教师简介，在授课程等；

* **授课机构页面**（首页->授课机构）：授课机构列表，可按类别、地区进行筛选，可按学习人数、评论数进行排序，右侧上方为用户提交我要学习的咨询窗口，下方为机构的排名；
  * 授课机构详情页（首页->授课机构->机构）：该授课机构首页，可点击进行收藏，可分别进入机构课程、机构介绍、机构教师等页面；

* **个人中心页面**（首页->个人中心）：用户注册、登录、邮箱激活验证、密码找回、个人信息展示、修改页面，同时可分别进入我的课程、我的收藏、我的消息等页面；


## 二、环境搭建及包的安装
* 系统为OX10.11.6，如果使用其他系统，在安装pillow时，需要安装官网显示的适配版本
* python版本为3.6.5
* pip install virtualenv
* virtualenv venv
* source venv/bin/activate
* cd online
* pip install django
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
        说明：在授课机构右侧上方的提交窗口需要一张表来存储、课程评论表、收藏（课程、教师、机构）表、消息表、用户与课程之间的关系表


## 五、后台管理系统-Xadmin
* 不建议直接使用pip install xadmin，可能会由于django的不匹配而重新安装低版本的django  
        安装方法（使用源码，将第三方包作为应用注册）：
          
        在项目目录下新建extra_apps文件夹，存放第三方拓展包
        git clone -b django2 https://github.com/sshwsfc/xadmin.git
        将下载包中的xadmin文件夹移动到extra_apps文件夹，其他的删除
        在项目settings.py文件添加
        sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
        同时要进行注册xadmin和crispy_forms

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


## 项目流程：
* 一、分析前端提供的html文件，列出页面结构，确定需要创建的apps；
* 二、创建环境、配置数据库参数、创建apps；
* 三、根据页面内容，创建各apps的models；
* 四、使用xadmin管理后台
* 五、各功能模块实现：
    * 1.注册功能的实现：  
    注册流程:
    ![register](https://github.com/myminwang/online/blob/master/static/images/register.001.jpeg "register")
    * 用到的技术：
        * A.django自带的form验证功能，可以在处理用户提交的数据之前，进行数据格式等验证；
        * B.验证码技术，采用第三方验证码生成包captcha，在setting中配置添加app，配置url，在数据库中创建表后就可以使用了，在网页中、form中做好配置就行，自动实现验证过程，实现验证码功能；
    * 2.邮箱验证功能的实现：
        * A.邮件发送功能，使用django自带的send_mail模块，在setting中配置默认参数及自定义参数，创建通用模块文件夹，
        单独新建邮件发送模块，并使用随机函数生成随机的验证码，加在链接中，发给用户；
        * B.激活验证功能，用户点击激活链接后，后台判断是否为有效链接，成功激活后，将验证码做逻辑删除。
    * 3.登录、登录状态保持、登出功能实现：
        * 用户输入登录信息后，可登录账户并保持登录状态。
        * A.登录验证技术，使用authenticate方法，并重写该方法（在django.contrib.auth.backends.ModelBackend模块中），使之可以验证邮箱登录方式。
        * B.登录状态保持，登录验证通过后，使用login()方法，接收两个参数(request,user)，在session中生成_auth_user_id和_auth_user_backend两个键值，并发到客户端作为cookie，
        用户页面中的cookie添加sessionid的键值对（将该键值对复制到未登录的客户端，会变成登录状态），前端页面可通过{% if request.user.is_authenticated %}判断是否登录。
        * C.使用logout()方法，接收一个参数，退出登录后，会删除用户页面cookie中的sessionid键值对。
    * 4.密码找回功能：
        用户忘记密码时，可通过邮箱验证进行密码重置。
    * 5.筛选功能（机构列表页点击机构类型、城市，实现按需筛选功能）：  
    可对指定的类型、城市进行刷选，显示筛选条件、结果条数、结果。
        * A.显示筛选条件，在前端页面对指定字段进行判断，根据结果进行显示；
        * B.过滤器技术，根据指定条件（前端页面GET方式返回的city、ct值），对对象(all_orgs)使用filter()方法进行筛选，使用filter是为了避免没有匹配结果时（返回空），不会报错，
    并将结果（对象格式）返回给指定变量，变量在前端页面进行遍历，得结果；
        * C.其他，使用order_by()方法进行指定条件的排序，使用count()方法进行统计条数，使用[:]切片进行取值；
    * 6.排名功能：  
    实现对机构进行排名，并显示所在地等；
    * 7.分页功能：  
    对页面内容进行分页显示，可指定每页显示条数、页面显示样式等；
        * A.使用第三方pure_pagination应用，在配置中对页面显示样式进行设置，在视图中对分页的内容、每页显示条数进行配置，将进过分页处理的后对象传给前端，
        在前端进行内容显示的细微调整，如第一页不显示'上一页'、最后一页不显示'下一页'、当前页不显示链接等。
    * 8.用户咨询功能实现：
    在不刷新页面的情况下，完成用户咨询内容的提交、保存。
        * A.jQuery.ajax，监听用户咨询窗口，使用.ajax()函数将用户提交的数据以post的请求方式提交到后台服务器，服务器对数据处理后返回处理结果(以json格式)，ajax以智能方式判断传回的数
        据（不指定dataType值），通过回调函数success(),判断显示的结果，从而在不刷新整个页面的情况下处理用户提交的数据。
    * 9.课程机构首页、机构教师、机构课程、机构简介展示：
        * A.一对多数据引用，在处理E-R设计模型的MySQL数据库中，一对多关系的外键存储在"多的"一方，而"为一"的一方需要引用"多的"一方的数据时，
        使用类名小写_set方式，并且对引用的数据可以进行all(),get(),filter(),count(),order_by()等数据处理的操作,在前端可直接通过外键获取数据，如org.city.name
        * B.HTML过滤器，语法：{ { 变量|过滤器 }}，在前端处理数据时可以非常便捷的获取所需的数据，例如本项目中从服务器传到前端的request中提取特定数据
        进行判断，代码为{% ifequal request.path|slice:'13' '/org/org_home' %}，
    
        




## 待解决问题：
* xadmin，后台管理不能显示APP的中文名称
        每个APP文件下的__init__.py文件添加（以uses为例）：

        default_app_config = "users.apps.UsersConfig"

        使用runserver或makemigrations时，报错：
        ModuleNotFoundError: No module named 'users'
* 注册页面第一次显示时，不能显示验证码，点击注册并登录后可以正常显示:已解决，get方式调用视图时，需要将验证码模块render到网页中
* 用户咨询的手机号正则验证
* 后台管理中，对机构进行修改时，需要重新上传图片
* organizations.views的110行，是否可以调用方法进行排序，models中定义

        def course_nums(self):
        """课程数量"""
        return self.courseinfo_set.count()

* 
## 待优化项目：
* 邮件发送成功页面、密码修改页面，优化
* 注册页面输入框中显示None，value=register_form.email.value，一开始没有返回值的原因，如何消除，现在把value注释了，不能显示红框
* 直接输入网址链接，是否能直接进入相应页面？
* org-list.html 的第44行不理解，第88、89行待修改
* 机构列表页，城市选择后不变色，分页的页面显示不正常,已解决，原因是前端页面使用for遍历城市，city的取值为变量，当没有取值时，返回后端'None',而不是''。
* 添加添加模块，要高大上的那种
* 机构首页的机构介绍，限定字数（过滤器）
* 教师列表页——教师分享功能
* '更多'菜单展开项

* 收藏：机构首页、教师详情页

* 课程、教师、机构的点击数处理



* 服务器启动项目
* /etc/init.d/nginx restart
* uwsgi --http :8000 --plugin python --module Online_learning.wsgi
