from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Myuser
from django.contrib.auth.hashers import make_password
import random
import smtplib
from email.mime.text import MIMEText

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

def register_index(request):
    if request.method == "POST":
        user_id = request.POST.get("user_name")

        messages.add_message(request,messages.SUCCESS,'test')
    return render(request,"register.html")
#注册函数
def register(request):

    name = str(request.POST.get("user_name"))
    if(name=='1') :
        return HttpResponse(name)
    else:
        name = None
        return HttpResponse(name)

#用于向用户邮箱发送验证码邮件的函数
def sendVcode(request):
    email = str(request.GET.get("user_email"))
    vcode = get_vcode()
    print(email)
    send_sample_email(vcode=vcode, receiver=email)
    code = make_password(vcode)
    print(vcode,code)
    return HttpResponse(code)

#用于获得6位验证码的函数
def get_vcode():
    result = ''
    for i in range(6):
        num = random.randint(0,9)
        result += str(num)
    return result

#用于向指定邮箱发送验证码的函数
def send_sample_email(vcode,receiver,title="现代服务业发展水平评估系统验证码",):
    #设置服务器所需信息
    #163邮箱服务器地址
    mail_host = 'smtp.163.com'
    #163用户名
    mail_user = 'esdlmsi'
    #密码(部分邮箱为授权码)
    mail_pass = 'FWYKVFDIYPDFTXBK'
    #邮件发送方邮箱地址
    sender = 'esdlmsi@163.com'
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = [receiver]
    content="验证码为："
    content += vcode
    #设置email信息
    #邮件内容设置
    message = MIMEText(content,'plain','utf-8')
    #邮件主题
    message['Subject'] = title
    #发送方信息
    message['From'] = sender
    #接受方信息
    message['To'] = receivers[0]

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass)
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string())
        #退出
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误
