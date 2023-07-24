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
from django.urls import path
import myUser.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',myUser.views.login),
    path('register/',myUser.views.register_index),
    path('register_handle/',myUser.views.register),
    path('sendVcode',myUser.views.sendVcode)
    ]
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