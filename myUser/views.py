from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Myuser
from django import forms

# Create your views here.
def login(request):
    if request.method == "POST":

        user_id = request.POST.get("user_id")
        user_pwd = request.POST.get("user_pwd")
        user_type = str(request.POST.get('user_type'))
        tempuser = None
        if Myuser.objects.filter(id=user_id):
            tempuser = Myuser.objects.get(id=user_id)
        elif Myuser.objects.filter(email=user_id):
            tempuser = Myuser.objects.get(email=user_id)
        else :
            messages.add_message(request,messages.WARNING,'用户不存在！')

        if tempuser is not None :
            if tempuser.type == user_type:
                user = authenticate(username = user_id, password = user_pwd)
                if user is not None :
                    auth.login(request,user)
                    messages.add_message(request,messages.SUCCESS,'登录成功！')
                    return redirect('/')
                else :
                    messages.add_message(request,messages.WARNING,'密码错误！请重新输入！')
            else:
                messages.add_message(request, messages.WARNING, '用户类型错误！')

    return render(request, "login.html")

