"""esdlmsi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
import myUser.views
import dataHandler.views
urlpatterns = []

##以下为有关myUser类的url（即用户信息有关的功能）
myUser_urls = [
    #以下为未登录情况下的登录、注册、找回密码相关url
    path('admin1/', admin.site.urls),
    path('login/',myUser.views.login),
    path('',myUser.views.login),
    path('index/', myUser.views.login),
    path('register/',myUser.views.register),
    #path('register_handle/',myUser.views.register),
    path('sendVcode',myUser.views.sendVcode),
    path('sendVcode2', myUser.views.sendVcode2),
    path('resetVerify',myUser.views.resetVerify),
    path('reset',myUser.views.reset),
    path('logout',myUser.views.logout),

    #以下为不同类型用户主页跳转的url
    path('admin/',myUser.views.admin_index),
    path('ent/',myUser.views.ent_index),
    path('gov/',myUser.views.gov_index),

    #以下为管理员用户管理功能相关的url
    path('admin/user_manage/',myUser.views.user_manage),
    path('admin/get_pageinfo',myUser.views.get_pageinfo),
    path('admin/search_pageinfo',myUser.views.search_pageinfo),
    path('admin/delete_singleinfo',myUser.views.delete_singleinfo),
    path('admin/update_singleinfo',myUser.views.update_singleinfo),
    path('admin/delete_pageinfo',myUser.views.delete_pageinfo),

    #以下为用户页面中心的返回url
    path('personal_infor/',myUser.views.personal_info),
    path('update_personalinfo/',myUser.views.update_personalinfo),

    ]
urlpatterns += myUser_urls

##以下为有关dataHandler类的url（即数据处理有关的功能）
dataHandler_urls =[

    #以下为数据上传有关的url
    path('ent/data_upload',dataHandler.views.ent_upload_data),

    ]

urlpatterns += dataHandler_urls

'''
    path('',views.login),
    path("index/",views.index),
    #path
    path("index/normal/",views.index_normal),
    path("data_upload/",views.test),
    path("index_ent",views.index_ent),
    path("index_gov", views.index_gov),
    path("index_admin",views.index_admin)
    
]
'''