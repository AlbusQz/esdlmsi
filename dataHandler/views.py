from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse,Http404
from django.contrib.auth.models import User
import os
import csv
import pandas as pd
from myUser.models import Myuser

# Create your views here.
#测试函数
@login_required
def ent_uploadData(request):
    return render(request,'data_handler/ent_data_upload.html')

#企业用户下载文件模板函数
@login_required
def ent_downloadSample(request):
    file_path = "static/file/sample.xlsx"
    try:
        f = open(file_path,'rb')
        r = FileResponse(f,as_attachment=True,filename="sample.xlsx")
        return r
    except Exception:
        raise Http404("Download error")

#企业用户上传文件函数
@login_required
def ent_getUpload(request):
    if request.method == "POST":
        tempuser = request.user
        #tempmyUser = Myuser.objects.get(u=tempuser)
        #type =
        print(tempuser.username)
        print(request.FILES)
        tempfile = request.FILES.get('file',None)
        if not tempfile:
            print("File not found!")
            return HttpResponse('file not found')
        else:
            toppath = "static/file/tempfile/ent/"
            endpath = tempuser.username + "/"
            path = toppath+endpath
            if not os.path.exists(path):
                os.makedirs(path)
            filename = tempfile.name
            if(filename[-3:] == "csv"):
                temp_data = pd.read_csv(tempfile.file,encoding='UTF-8')
                temp_data.to_csv(path+filename,encoding='utf_8_sig')
                print(temp_data)
            else:
                print('haha')
                temp_data = pd.read_excel(tempfile.file)
                temp_data.to_excel(path+filename,encoding='utf_8_sig')
                print(temp_data)
            #csv_writer = csv.writer(tempfile.file)
            #csv_writer.
            print(tempfile.name)
            print('nice!')
            return HttpResponse("文件"+filename+"上传成功!")


#企业用户数据输入函数
@login_required
def ent_inputData(request):

    return render(request,'data_handler/ent_data_input.html')