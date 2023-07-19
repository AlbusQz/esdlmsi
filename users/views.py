from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Users
from django.contrib import messages
from django.http import HttpResponseRedirect


# Create your views here.z

def testloginpage(request):
    users = Users.objects.all()
    user_list = list()
    for count, user in enumerate(users):
        user_list.append(str(user.id) + "&nbsp" + str(user.type) + "<br>")
    return HttpResponse(user_list)


def login(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user_pwd = request.POST.get("user_pwd")

        if Users.objects.filter(id=user_id):
            tempuser = Users.objects.get(id=user_id)
            if tempuser.password == user_pwd:
                messages.success(request, "登录成功")
                print(tempuser.type)
                if tempuser.type == "企业/政府用户":
                    print("here")
                    return redirect("/index/normal/", {"user": tempuser})
                elif tempuser.type == "管理员用户":
                    redirect("/index_admin/", {"user": tempuser})
                elif tempuser.type == "行业专家用户":
                    redirect("/index_expert/", {"user": tempuser})
                else :
                    messages.error(request, "用户类型出现错误，请检查数据库！")

            else:
                messages.error(request, message="密码错误！")
                # return HttpResponse("密码错误")

        else:
            messages.error(request, message="用户不存在！")
            # return HttpResponse("用户不存在")
    return render(request, "login.html")

def index_normal(request):
    return render(request,"index_normal.html")

def index(request):
    return render(request, "index.html", )

def test(request):
    return render(request,"data_upload.html")

