from django.shortcuts import render
from django.http import HttpResponse
from .models import Users


# Create your views here.z

def testloginpage(request):
    users = Users.objects.all()
    user_list = list()
    for count,user in enumerate(users):
        user_list.append(str(user.id)+"&nbsp"+str(user.type)+"<br>")
    return HttpResponse(user_list)

def login(request):

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user_pwd = request.POST.get("user_pwd")

        if Users.objects.filter(id=user_id) :
            if Users.objects.get(id=user_id).password == user_pwd:
                return HttpResponse("登录成功")
            else:
                return HttpResponse("密码错误")
        else:
            return HttpResponse("用户不存在")
    return render(request,"login.html")

def index(request):
    return render(request,"index.html",)

def captcha_gen():
    return