from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages
from .models import Myuser
from django.contrib.auth.hashers import make_password, check_password
import random
import smtplib
from email.mime.text import MIMEText
import json
from django.contrib.auth.models import User
import pytz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required

path_dict = {
    '企业用户':"/ent/",
    '政府用户':'/gov/',
    '管理员用户':'/admin/'
}

# Create your views here.
# 处理登录过程的函数
def login(request):
    auth.logout(request)
    temp ={}
    if request.method == "POST":

        user_id = request.POST.get("user_id")
        user_pwd = request.POST.get("user_pwd")
        user_type = str(request.POST.get('user_type'))
        tempuser = None
        if Myuser.objects.filter(email=user_id):
            tempuser = Myuser.objects.get(email=user_id)
            user_id = tempuser.id
        elif Myuser.objects.filter(id=user_id):
            tempuser = Myuser.objects.get(id=user_id)
        else:
            messages.add_message(request, messages.WARNING, '用户不存在！')

        if tempuser is not None:
            if tempuser.type != "专家用户":
                print(tempuser.type)
                if tempuser.type == user_type:
                    user = authenticate(username=user_id, password=user_pwd)
                    if user is not None:
                        auth.login(request, user)
                        type = tempuser.type
                        if type == '管理员用户':
                            return redirect('/admin/')
                        elif type == '企业用户':
                            return redirect('/ent/')
                        elif type == '政府用户':
                            return redirect('/gov/')
                        else :
                            messages.add_message(request,messages.ERROR,'用户类型出现错误！！请联系管理员')
                            return redirect('/')
                    else:
                        messages.add_message(request, messages.WARNING, '密码错误！请重新输入！')
                else:
                    messages.add_message(request, messages.WARNING, '用户类型错误！')

            else:
                user = authenticate(username=user_id, password=user_pwd)
                if user is not None:
                    auth.login(request, user)
                    # messages.add_message(request, messages.SUCCESS, '登录成功！')
                    type = user_type
                    if type == '管理员用户':
                        return redirect('/admin/')
                    elif type == '企业用户':
                        return redirect('/ent/')
                    elif type == '政府用户':
                        return redirect('/gov/')
                    else:
                        messages.add_message(request, messages.ERROR, '用户类型出现错误！！请联系管理员')
                        return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '密码错误！请重新输入！')


    return render(request, "login.html")

# 注册功能函数
def register(request):
    # if request.method == "POST":
    #    user_id = request.POST.get("user_name")
    auth.logout(request)
    if request.method == "POST":
        user_pwd = request.POST.get("user_pwd")
        user_type = str(request.POST.get('user_type'))
        user_name = request.POST.get("user_name")
        user_email = request.POST.get("user_email")
        v_code = request.POST.get("v_code")
        h_code = request.POST.get("h_code")
        if Myuser.objects.filter(email=user_email):
            messages.add_message(request, messages.ERROR, '该邮箱已被注册过了，请更换后重新注册！')
        else:
            if check_password(v_code, h_code):
                now = datetime.now(pytz.timezone('Asia/Shanghai'))
                format_time = now.strftime('%Y-%m-%d %H:%M:%S')
                tempMyuser = Myuser(password=user_pwd, email=user_email, type=user_type, name=user_name,
                                    create_time=format_time)
                print(tempMyuser.id)
                tempMyuser.save()
                tempid = tempMyuser.id

                tempUser = User(username=tempid, password=make_password(user_pwd))
                tempUser.save()
                tempMyuser.u_id = tempUser.id
                tempMyuser.save()
                messages.add_message(request, messages.SUCCESS, "注册成功！，您的ID为" + str(tempid) + "，请牢记。")
                messages.add_message(request, messages.SUCCESS, "接下来将跳转至登录界面")

                return redirect("/login")

            else:
                messages.add_message(request, messages.ERROR, '验证码错误，请重新注册！')
    #    messages.add_message(request, messages.SUCCESS, 'test')
    return render(request, "register.html")

# 注销函数
def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, '退出登录！')
    return redirect("/login")

# 注册函数（测试用，已停用）
def register_index(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user_pwd = request.POST.get("user_pwd")
        user_type = str(request.POST.get('user_type'))
        user_name = request.POST.get("user_name")
        user_email = request.POST.get("user_email")
        v_code = request.POST.get("v_code")
        h_code = request.POST.get("h_code")
        if check_password(v_code, h_code):

            tempMyuser = Myuser(password=user_pwd, email=user_email, type=user_type, name=user_name)
            print(tempMyuser.id)
            tempMyuser.save()
            tempid = tempMyuser.id

            tempUser = User(user_name=tempid, password=user_pwd)
            tempUser.save()
            tempMyuser.u_id = tempUser.id
            tempMyuser.save()
            tempid = tempMyuser()

        else:
            messages.add_message(request, messages.ERROR, '验证码错误，请重新注册！')

    name = str(request.POST.get("user_name"))
    if (name == '1'):
        return HttpResponse(name)
    else:
        name = None
        return HttpResponse(name)


# 修改密码功能中确认用户存在的函数
def resetVerify(request):
    if request.method == "POST":
        user_email = request.POST.get("user_email")
        v_code = request.POST.get("v_code")
        h_code = request.POST.get("h_code")
        if Myuser.objects.filter(email=user_email):
            tempMyuser = Myuser.objects.get(email=user_email)
            if check_password(v_code, h_code):
                request.session['user_id'] = tempMyuser.id
                return redirect("/reset")
            else:
                messages.add_message(request, messages.ERROR, '验证码错误，请重新输入！')
        else:
            messages.add_message(request, messages.ERROR, '不存在该用户，请重新输入！')
    return render(request, "resetVerify.html")


# 修改密码功能中执行密码修改的函数
def reset(request):

    if 'user_id' in request.session:
        user_id = request.session['user_id']
        #del request.session['user_id']
        print("here")

        if Myuser.objects.filter(id=user_id):
            if request.method == 'POST':
                user_pwd_new = request.POST.get("user_pwd")
                check_pwd = request.POST.get("")
                tempMyuser = Myuser.objects.get(id=user_id)
                tempUser = tempMyuser.u
                if check_password(user_pwd_new, tempUser.password):
                    messages.add_message(request, messages.ERROR, "密码与上次相同，请重新输入新的密码")
                # elif
                else:
                    tempUser.password = make_password(user_pwd_new)
                    tempMyuser.password = user_pwd_new
                    tempUser.save()
                    tempMyuser.save()
                    messages.add_message(request, messages.SUCCESS, "ID为" + str(user_id) + "的账号的密码重置成功！")
                    messages.add_message(request, messages.SUCCESS, "接下来将跳转至登录界面")
                    del request.session['user_id']
                    return redirect("/login")
        else:
            messages.add_message(request, messages.ERROR, "session出现错误")
            return redirect("/login")
    else:
        return redirect("/login")
    return render(request, "reset.html")


# 用于在注册功能中向用户邮箱发送验证码邮件的函数
def sendVcode(request):
    print('test')
    email = str(request.POST.get("user_email"))
    if Myuser.objects.filter(email=email):
        data = {'status': 0, 'code': '此邮箱已被注册过！'}
        json_data = json.dumps(data)
        return JsonResponse(json_data, safe=False)
    else:
        vcode = get_vcode()
        print(email)
        send_sample_email(vcode=vcode, receiver=email)
        code = make_password(vcode)
        print(vcode, code)
        data = {"status": "1", "code": code}
        json_data = json.dumps(data)
        print(json_data)
        return JsonResponse(json_data, safe=False)


# 用于在重置密码功能中向用户邮箱发送验证码邮件的函数
def sendVcode2(request):
    email = str(request.POST.get("user_email"))
    if Myuser.objects.filter(email=email):
        vcode = get_vcode()
        send_sample_email(vcode=vcode, receiver=email)
        code = make_password(vcode)
        print(vcode, code)
        data = {"status": "1", "code": code}
        json_data = json.dumps(data)
        print(json_data)
        return JsonResponse(json_data, safe=False)
    else:
        data = {'status': 0, 'code': '此邮箱不存在！'}
        json_data = json.dumps(data)
        return JsonResponse(json_data, safe=False)


# 用于获得6位验证码的函数
def get_vcode():
    result = ''
    for i in range(6):
        num = random.randint(0, 9)
        result += str(num)
    return result


# 用于向指定邮箱发送验证码的函数
def send_sample_email(vcode, receiver, title="现代服务业发展水平评估系统验证码", ):
    # 设置服务器所需信息
    # 163邮箱服务器地址
    mail_host = 'smtp.163.com'
    # 163用户名
    mail_user = 'esdlmsi'
    # 密码(部分邮箱为授权码)
    mail_pass = 'FWYKVFDIYPDFTXBK'
    # 邮件发送方邮箱地址
    sender = 'esdlmsi@163.com'
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = [receiver]
    content = "验证码为："
    content += vcode
    # 设置email信息
    # 邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = title
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]

    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误


# 处理用户权限的中间件
class UserAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 在每个请求之前进行组权限判断
        print("test1")
        flag, path = self.check_type_auth(request)
        paths = [
            "/login/",
            "/register/",

        ]
        if flag == False:
            print('test')
            messages.add_message(request, messages.ERROR, "无访问权限，正在重定向")
            return redirect(path)
        else:
            return self.get_response(request)

    def check_type_auth(self, request):
        # 获取当前请求的用户对象
        user = request.user
        # 获取当前请求的路径
        path = request.path
        login_flag = user.is_authenticated
        # 设置需要进行限制访问的路径列表和对应的组
        restricted_paths = {
            'url存在的路径': '对应的组名',
            # 拿刚才创建的group1来举例
            '/ent/': '企业用户',
            '/ent': '企业用户',
            '/gov/': '政府用户',
            '/gov': '政府用户',
            '/admin/': '管理员用户',
            '/admin': '管理员用户',

            ## 以下专门用于专家用户：
            '/ent/': '专家用户',
            '/ent': '专家用户',
            '/gov/': '专家用户',
            '/gov': '专家用户',
            '/admin/': '专家用户',
            '/admin': '专家用户',

        }
        go_path = '/login'
        type = "未登录"
        if login_flag:
            tempMyuser = Myuser.objects.get(u=user)
            type = tempMyuser.type
            if type == "企业用户":
                go_path = "/ent/"
            elif type == "政府用户":
                go_path = "/gov/"
            else:
                go_path = "/admin"

        # 检查用户是否属于指定组，并判断是否允许访问特定页面
        for restricted_path, restricted_type in restricted_paths.items():
            # print(restricted_path,restricted_type,path)
            # print(restricted_path in path,restricted_type!=type)
            if restricted_path in path and (restricted_type != type or user.is_authenticated == False):
                return False, go_path

        return True, path


# 返回用户管理模块界面的函数
def user_manage(request):
    return render(request, "user_manage.html")


# 返回用户信息并进行分页的函数
def get_pageinfo(request):
    data = Myuser.objects.all()
    dataCount = data.count()
    pageIndex = request.GET.get('pageIndex')
    pageSize = request.GET.get('pageSize')

    list = []
    res = []
    for item in data:
        dict = {}
        dict['id'] = item.id
        dict['name'] = item.name
        dict['email'] = item.email
        dict['mobile'] = item.mobile
        dict['type'] = item.type
        dict['createtime'] = item.create_time.strftime('%Y-%m-%d %H:%M:%S')
        #print(dict['creatime'])
        list.append(dict)
    #print(pageIndex)
    #print(pageSize)
    pageInator = Paginator(list, pageSize)
    context = pageInator.page(pageIndex)
    for item in context:
        res.append(item)
    result = {
        'code': 0,
        'msg': 'nice',
        'DataCount': dataCount,
        'data': res
    }
    return HttpResponse(json.dumps(result))

#用户管理功能中的模糊搜索函数
def search_pageinfo(request):

    params = request.GET.get('searchParams')
    params = json.loads(params)
    q = Q()
    id = params['id']
    if(id!=''):
        q = q&Q(id__contains=id)
    name = params['name']
    if (name != ''):
        q = q & Q(name__contains=name)
    email = params['email']
    if (email != ''):
        q = q & Q(email__contains=email)
    mobile = params['mobile']
    if (mobile != ''):
        q = q & Q(mobile__contains=mobile)
    type = params['type']
    if (type != ''):
        q = q & Q(type__contains=type)
  #  q = Q(name__contains=name)&Q(email__contains=email)&Q(mobile__contains=mobile)&Q(type__contains=type)

    data = Myuser.objects.filter(q)
    dataCount = data.count()
    pageIndex = request.GET.get('pageIndex')
    pageSize = request.GET.get('pageSize')

    list = []
    res = []
    for item in data:
        dict = {}
        dict['id'] = item.id
        dict['name'] = item.name
        dict['email'] = item.email
        dict['mobile'] = item.mobile
        dict['type'] = item.type
        dict['createtime'] = item.create_time.strftime('%Y-%m-%d %H:%M:%S')
        #print(dict['creatime'])
        list.append(dict)
    #print(pageIndex)
    #print(pageSize)
    pageInator = Paginator(list, pageSize)
    context = pageInator.page(pageIndex)
    for item in context:
        res.append(item)
    result = {
        'code': 0,
        'msg': 'nice',
        'DataCount': dataCount,
        'data': res
    }
    return HttpResponse(json.dumps(result))

#用户管理功能中的删除单行数据的功能函数
def delete_singleinfo(request):
    get_id = request.GET.get('id')
    Myuser.objects.filter(id = get_id).delete()
    return HttpResponse('nice')

#用户管理功能中的删除多行数据的功能函数
def delete_pageinfo(request):
    #get_id = request.GET.get('id')
    params = request.GET.get('searchParams')
    params = json.loads(params)
    for param in params:
        tempid = param['id']
        print(tempid)
        Myuser.objects.filter(id = tempid).delete()
    #Myuser.objects.filter(id = get_id).delete()
    return get_pageinfo(request)


#用户管理功能中的修改单行数据的功能函数
def update_singleinfo(request):
    get_id = request.GET.get('id')
    name = request.GET.get('name')
    email = request.GET.get('email')
    mobile = request.GET.get('mobile')
    type = request.GET.get('type')
    temp = Myuser.objects.get(id = get_id)
    if(name!=""):
        temp.name = name
    if(email!=""):
        temp.email = email
    if(mobile!=''):
        temp.mobile = mobile
    if(type!=''):
        temp.type = type
        temp.save()
    #Myuser.objects.filter(id = get_id).delete()
    return HttpResponse('nice')

#用来返回企业用户主页的函数
def ent_index(request):
    user = request.user
    tempuser = Myuser.objects.get(u=user)
    id = tempuser.id
    name = tempuser.name
    type = tempuser.type
    type = json.dumps(type)
    type1 = "政府用户界面"
    path1 = '/gov/'
    type2 = "管理员用户界面"
    path2 = '/admin/'
    return render(request, "index_ent.html",locals())

#用来返回政府用户主页的函数
def gov_index(request):
    user = request.user
    tempuser = Myuser.objects.get(u=user)
    id = tempuser.id
    name = tempuser.name
    type = tempuser.type
    type = json.dumps(type)
    type1 = "企业用户界面"
    path1 = '/ent/'
    type2 = "管理员用户界面"
    path2 = '/admin/'
    return render(request, "index_gov.html",locals())

#用来返回管理员用户主页的函数
def admin_index(request):
    user = request.user
    tempuser = Myuser.objects.get(u=user)
    id = tempuser.id
    name = tempuser.name
    type = tempuser.type
    type = json.dumps(type)
    type1 = "企业用户界面"
    path1 = '/ent/'
    type2 = "政府用户界面"
    path2 = '/gov/'
    return render(request, "index_admin.html",locals())

#用于返回用户个人信息界面的函数
@login_required
def personal_info(request):
    user = request.user
    tempuser = Myuser.objects.get(u=user)
    id = tempuser.id
    name = tempuser.name
    email = tempuser.email
    type = tempuser.type
    phone = tempuser.mobile
    ctime = tempuser.create_time.strftime('%Y-%m-%d %H:%M:%S')
    del user
    del tempuser
    return render(request,'personal_info.html',locals())

#用于修改用户个人信息的函数
@login_required
def update_personalinfo(request):
    user = request.user
    tempuser = Myuser.objects.get(u=user)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('phone')
        v_code = request.POST.get("v_code")
        h_code = request.POST.get("h_code")
        if email!=tempuser.email:
            if check_password(v_code, h_code):
                tempuser.email=email
                tempuser.name=name
                tempuser.mobile=mobile
                tempuser.save()
                messages.add_message(request,messages.SUCCESS,'修改成功！')
            else:
                messages.add_message(request, messages.ERROR, '验证码错误，请重新输入！')
        else:
            tempuser.name = name
            tempuser.mobile = mobile
            tempuser.save()
            messages.add_message(request, messages.SUCCESS, '修改成功！')
    return redirect('/personal_infor/')

# 单纯的测试函数
def test(request):
    return render(request, "index_admin.html")


#返回主页的函数
def get_main(request):
    user = request.user
    tempuser = Myuser.objects.get(u=user)
    if tempuser.type == '企业用户':
        url = 'main_ent.html'
    elif tempuser.type == '政府用户':
        url = 'main_gov.html'
    elif tempuser.type == '管理员用户':
        url = 'main_admin.html'
    elif tempuser.type == '专家用户':
        url = 'main.html'
    return render(request, url)