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
import myProcess.views
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
    path('main/',myUser.views.admin_index),

    #以下为返回主页的url
    path('admin/index/',myUser.views.get_main),
    path('ent/index/',myUser.views.get_main),
    path('gov/index/',myUser.views.get_main),

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
    path('ent/data_upload',dataHandler.views.ent_uploadData),
    path('ent/sample_data_download',dataHandler.views.ent_downloadSample),
    path('ent/uploadFile',dataHandler.views.ent_getUpload),

    #以下为数据输入有关的url
    path('ent/data_input',dataHandler.views.ent_inputData),

    #以下为数据查询有关的url
    path('ent/data_search',dataHandler.views.get_ent_research),
    path('ent/get_ent_data',dataHandler.views.get_ent_data),
    path('ent/get_ent_data_all',dataHandler.views.get_ent_data_all),
    path('ent/get_data_detail/<int:id>/',dataHandler.views.get_ent_detail),
    path('ent/search_ent_info',dataHandler.views.search_ent_info),
    path('ent/search_ent_info_all', dataHandler.views.search_ent_info_all),
    path('ent/delete_ent_info', dataHandler.views.delete_ent_info),
    path('ent/get_data_updatepage/<int:id>/',dataHandler.views.get_ent_updatepage),
    path("ent/update_ent_info",dataHandler.views.ent_update_info),

    path('gov/data_search',dataHandler.views.get_ent_research),
    path('gov/get_ent_data',dataHandler.views.get_ent_data),
    path('gov/get_ent_data_all',dataHandler.views.get_ent_data_all),
    path('gov/get_data_detail/<int:id>/',dataHandler.views.get_ent_detail),
    path('gov/search_ent_info',dataHandler.views.search_ent_info),
    path('gov/search_ent_info_all', dataHandler.views.search_ent_info_all),
    path('gov/delete_ent_info', dataHandler.views.delete_ent_info),
    path('gov/get_data_updatepage/<int:id>/',dataHandler.views.get_ent_updatepage),
    path("gov/update_ent_info",dataHandler.views.ent_update_info),

    # 以下为数据预处理有关的url
    path('ent/data_process', dataHandler.views.get_ent_process),
    path('ent/get_ent_pre_data', dataHandler.views.get_ent_pre_data),
    path('ent/process_data', dataHandler.views.ent_process_data),
    path('admin/pre_params',dataHandler.views.admin_get_preparams),
    path('admin/update_preparams/',dataHandler.views.admin_update_preparams),


    # 以下为数据下载有关的url
    path('ent/data_download', dataHandler.views.ent_data_download),
    path("ent/download_singleinfo/<int:id>/",dataHandler.views.ent_download_singledata),
    path('ent/download_data',dataHandler.views.ent_download_data),


    ]

urlpatterns += dataHandler_urls

##以下为有关myProcess类的url（即分析过程有关的功能）
myProcess_urls = [

    #以下为生成处理过程有关的url
    path("ent/generate_process",myProcess.views.ent_generate_process),
    path('ent/process_history',myProcess.views.ent_get_processhistorypage),
    path('ent/get_process_his',myProcess.views.ent_get_processhis),
    path('ent/search_process_his',myProcess.views.ent_search_processhis),
    path('ent/delete_process_his',myProcess.views.delete_ent_process_his),
    path('ent/get_processhis_detail/<int:id>/',myProcess.views.get_ent_process_detail),
    path('ent/get_processhis_data/<int:id>',myProcess.views.get_ent_processhis_data),

    #temp
    path('ent/ent_analyse',myProcess.views.temp_get_select),
    path('gov/ent_analyse',myProcess.views.temp_get_select),
    path('admin/ent_analyse',myProcess.views.temp_get_select),

    path('ent/404',myProcess.views.temp_404),
    path('gov/404',myProcess.views.temp_404),
    path('admin/404',myProcess.views.temp_404),

    path('ent/404_2',myProcess.views.temp_404),
    path('gov/404_2',myProcess.views.temp_404),
    path('admin/404_2',myProcess.views.temp_404),

    path('ent/404_3',myProcess.views.temp_404),
    path('gov/404_3',myProcess.views.temp_404),
    path('admin/404_3',myProcess.views.temp_404),

    path('ent/404_4',myProcess.views.temp_404),
    path('gov/404_4',myProcess.views.temp_404),
    path('admin/404_4',myProcess.views.temp_404),
    # path('ent/delete_process_his',myProcess.views.delete_ent_process_his),
    # path('ent/delete_process_his',myProcess.views.delete_ent_process_his),

]

urlpatterns += myProcess_urls

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