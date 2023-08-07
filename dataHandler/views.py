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
from django.contrib import messages
from .models import EnterpriseInfo

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
                temp_data = pd.read_csv(tempfile.file,sep='\s|,|;',error_bad_lines = False,encoding='UTF-8')
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

    tempdata = []
    if request.method == "POST":
        request.POST._mutable= True
        form_data =[]
        print(request.POST.items())
        for key,value in request.POST.items():
            if value == "":
                print(key)
                #form_data
                request.POST[key] = None

        user = request.user
        tempuser = Myuser.objects.get(u=user)

        tempinfo = EnterpriseInfo()

        basic_name = request.POST.get('basic','')
        tempdata.append(basic_name)
        basic_code = request.POST.get('basic_code','')
        tempdata.append(basic_code)
        basic_date = request.POST.get('basic_date','')
        tempdata.append(basic_date)
        basic_fund = request.POST.get('basic_fund', 0)
        if basic_fund == '':
            basic_fund = 0
        tempdata.append(basic_fund)
        basic_fund_kind = request.POST.get('basic_fund_kind', '')
        tempdata.append(basic_fund_kind)
        basic_ind = request.POST.get('basic_ind', '')
        tempdata.append(basic_ind)
        basic_ind_code = request.POST.get('basic_ind_code', 0)
        if basic_ind_code == "":
            basic_ind_code = None
        tempdata.append(basic_ind_code)
        basic_IPO_time = request.POST.get('basic_IPO_time', '')
        tempdata.append(basic_IPO_time)
        basic_exchange = request.POST.get('basic_exchange', '')
        tempdata.append(basic_exchange)
        basic_reg_pro = request.POST.get('basic_reg_pro', '')
        tempdata.append(basic_reg_pro)
        basic_reg_city = request.POST.get('basic_reg_city', '')
        tempdata.append(basic_reg_city)
        basic_reg_area = request.POST.get('basic_reg_area', '')
        tempdata.append(basic_reg_area)
        basic_real_pro = request.POST.get('basic_real_pro', '')
        tempdata.append(basic_real_pro)
        basic_real_city = request.POST.get('basic_real_city', '')
        tempdata.append(basic_real_city)
        basic_real_area = request.POST.get('basic_real_area', '')
        tempdata.append(basic_real_area)
        tempinfo.setBasic(tempdata)
        tempdata.clear()


        ser_field = request.POST.get('ser_field', '')
        #tempdata.append(ser_field)
        tempinfo.setScope(ser_field)

        peo_count1 = request.POST.get('peo_count1', 0)
        if peo_count1 == "":
            peo_count1 = 0
        tempdata.append(peo_count1)
        peo_count2 = request.POST.get('peo_count2', 0)
        if peo_count2 == "":
            peo_count2 = 0
        tempdata.append(peo_count2)
        tempinfo.setPeople(peo_count1,peo_count2)
        tempdata.clear()

        debt = request.POST.get('debt', 0)
        tempdata.append(debt)
        equity = request.POST.get('equity', 0)
        tempdata.append(equity)
        net_worth = request.POST.get('net_worth', 0)
        tempdata.append(net_worth)
        grate_total = request.POST.get('grate_total', 0)
        tempdata.append(grate_total)
        grate_bus = request.POST.get('grate_bus', 0)
        tempdata.append(grate_bus)
        tax = request.POST.get('tax', 0)
        tempdata.append(tax)
        tempinfo.setFinance()
        tempdata.clear()

        ip_total = request.POST.get('ip_total', 0)
        tempdata.append(ip_total)
        ap_total = request.POST.get('ap_total', 0)
        tempdata.append(ap_total)
        jp_total = request.POST.get('jp_total', 0)
        tempdata.append(jp_total)
        sp_total = request.POST.get('sp_total', 0)
        tempdata.append(sp_total)
        ns_total = request.POST.get('ns_total', 0)
        tempdata.append(ns_total)
        tempinfo.setPatent(tempdata)
        tempdata.clear()

        inforplat_total = request.POST.get('inforplat_total', 0)
        tempdata.append(inforplat_total)
        icp_total = request.POST.get('icp_total', 0)
        tempdata.append(icp_total)
        tempinfo.setInfromation(inforplat_total,icp_total)
        tempdata.clear()

        honor_total = request.POST.get('honor_total', 0)
        tempdata.append(honor_total)
        a_taxpayer = request.POST.get('a_taxpayer', '')
        tempdata.append(a_taxpayer)
        dishonesty = request.POST.get('dishonesty', '')
        tempdata.append(dishonesty)
        lawsuit_total = request.POST.get('lawsuit_total', 0)
        tempdata.append(lawsuit_total)
        is_ep = request.POST.get('is_ep', '')
        tempdata.append(is_ep)
        tempinfo.setHonor(tempdata)
        tempdata.clear()

        invest_time = request.POST.get('invest_time', 0)
        tempdata.append(invest_time)
        invest_amount = request.POST.get('invest_amount', 0)
        tempdata.append(invest_amount)
        bidding_time = request.POST.get('bidding_time', 0)
        tempdata.append(bidding_time)
        bidding_amount = request.POST.get('bidding_amount', 0)
        tempdata.append(bidding_amount)
        tempinfo.setInvest(invest_time,invest_amount,bidding_time,bidding_amount)

        tempinfo.mu = tempuser

        tempinfo.save()

        messages.add_message(request,messages.SUCCESS,"上传成功！")
        messages.add_message(request, messages.SUCCESS, "您可以在数据查询界面查询到这次的数据了！")
        return redirect("/ent/data_input")

    return render(request,'data_handler/ent_data_input.html')