import pytz

from django.core.paginator import Paginator
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
from .models import PreParams
import json
from django.db.models import Q
from dataHandler.VAEGAIN import VAE_GAIN
from dataHandler.SCIS import SCIS
from dataHandler.GAIN import GAIN
from sqlalchemy import create_engine
from dataHandler.models import Process

from django.db import connection
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
    user = request.user
    mu = Myuser.objects.get(u=user)
    if request.method == "POST":
        flag = False
        msg = ''
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
            #'''
            toppath = "static/file/tempfile/ent/"
            endpath = tempuser.username + "/"
            path = toppath+endpath
            '''
            if not os.path.exists(path):
                os.makedirs(path)
            '''
            filename = tempfile.name

            #conn = create_engine('mysql+pymysql://root:123456@localhost:3306/esdlmsi?charset=utf8')

            if(filename[-3:] == "csv"):
                try:
                    temp_data = pd.read_csv(tempfile.file,sep='\s|,|;',error_bad_lines = False)
                    #temp_data.fillna(value=None, inplace=True)
                    #temp_data = temp_data.where(temp_data.notnull(), None)
                    temp_data = temp_data.values.tolist()
                    #temp_data.to_sql("enterprise_info",con=conn,index = False , if_exists = 'append', chunksize = None)
                    #temp_data.to_csv(path+filename,encoding='utf_8_sig')

                    #print(temp_data)
                    #print(len(temp_data))
                    temp = []
                    for i in temp_data:
                        print(type(i[2]))
                        if i[2] != None and type(i[2]) == pd._libs.tslibs.timestamps.Timestamp:
                            i[2] = i[2].strftime('%Y-%m-%d')
                            print(i[2])
                        if i[7] != None and type(i[7]) == pd._libs.tslibs.timestamps.Timestamp:
                            i[7] = i[7].strftime('%Y-%m-%d')
                            #i[7] = str(i[7])
                        for j in range(len(i)):
                            # print(str(j)=="nan")
                            if str(i[j]) == "nan":
                                i[j] = None
                        # print(i)
                        flag, msg = EnterpriseInfo.isValid(i)
                        if flag :

                            temp = EnterpriseInfo()
                            temp.setAll(i)
                            if temp.getNeedpre():
                                temp.needpre = 1
                            else:
                                temp.needpre = 0
                            temp.mu = mu
                            temp.save()


                        print(flag)
                        print(msg)
                except Exception as e:
                    flag = False
                    msg = str(e)
                #print(temp)
                #print(temp[0]==float)
                #print(EnterpriseInfo.isValid(temp_data))
            else:
                #print('haha')
                #try:
                    temp_data = pd.read_excel(tempfile.file,)
                    temp_data = temp_data.values.tolist()

                    for i in temp_data:
                        if i[2] != None and type(i[2]) == pd._libs.tslibs.timestamps.Timestamp:
                            i[2] = i[2].strftime('%Y-%m-%d')
                            print(i[2])
                        if i[7] != None and type(i[7]) == pd._libs.tslibs.timestamps.Timestamp:
                            i[7] = i[7].strftime('%Y-%m-%d')
                            #i[7] = str(i[7])
                        for j in range(len(i)) :
                            #print(str(j)=="nan")
                            if str(i[j])=="nan":
                                i[j] = None
                        #print(i)
                        flag, msg = EnterpriseInfo.isValid(i)
                        if flag:

                            temp = EnterpriseInfo()
                            temp.setAll(i)
                            if temp.getNeedpre():
                                temp.needpre = 1
                            else:
                                temp.needpre = 0
                            temp.mu = mu
                            temp.save()


            if flag :
                return HttpResponse("文件"+filename+"上传成功!")
            else:
                return HttpResponse("文件" + filename + "上传失败!失败原因："+msg)

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

        basic_name = request.POST.get('basic_name','')
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

        now = datetime.now(pytz.timezone('Asia/Shanghai'))
        format_time = now.strftime('%Y-%m-%d %H:%M:%S')
        tempinfo.create_time = format_time

        if tempinfo.getNeedpre():
            tempinfo.needpre = 1
        else:
            tempinfo.needpre = 0

        tempinfo.save()

        messages.add_message(request,messages.SUCCESS,"上传成功！")
        if tempinfo.getNeedpre():
            messages.add_message(request, messages.WARNING, "输入的数据存在空缺数据项，需要进行预处理！")
        else:
            messages.add_message(request, messages.SUCCESS, "您可以在数据查询界面查询到这次的数据了！")
        return redirect("/ent/data_input")

    return render(request,'data_handler/ent_data_input.html')

#用于向企业用户返回数据查询页面的函数
@login_required
def get_ent_research(request):
    return render(request,"data_handler/ent_data_search.html")

#用于向企业用户数据查询界面返回数据的函数
@login_required
def get_ent_data(request):
    user = request.user
    myuser = Myuser.objects.get(u=user)
    data = EnterpriseInfo.objects.filter(mu=myuser,needpre=0)
    dataCount = data.count()
    pageIndex = request.POST.get('pageIndex')
    pageSize = request.POST.get('pageSize')

    list = []
    res = []
    for item in data:
        dict = {}
        dict['t_id'] = item.id
        dict['name'] = item.enterprise_name
        dict['id'] = item.enterprise_id
        if item.founding_date != None:
            dict['c_date'] = item.founding_date.strftime('%Y-%m-%d')
        dict['fund'] = item.registered_capital
        dict['fund_kind'] = item.registered_capital_currency
        dict['ind_code'] = item.industry_code
        if item.time_to_market != None:
            dict['ipo_time'] = item.time_to_market.strftime('%Y-%m-%d')
        dict['exchange'] = item.bourse
        if item.registered_province !=None:
            dict['reg_add'] = item.registered_province+"/"+item.registered_city+"/"+item.registered_district
        if item.actual_province != None:
            dict['real_add'] = item.actual_province+"/"+item.actual_city+"/"+item.actual_district
        dict['c_time'] = item.create_time.strftime('%Y-%m-%d %H:%M:%S')
        list.append(dict)

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

#用于向企业用户数据查询界面返回所有数据的函数
@login_required
def get_ent_data_all(request):
    user = request.user
    myuser = Myuser.objects.get(u=user)
    data = EnterpriseInfo.objects.filter(mu=myuser)
    dataCount = data.count()
    pageIndex = request.POST.get('pageIndex')
    pageSize = request.POST.get('pageSize')

    list = []
    res = []
    for item in data:
        dict = {}
        dict['t_id'] = item.id
        dict['name'] = item.enterprise_name
        dict['id'] = item.enterprise_id
        if item.founding_date != None:
            dict['c_date'] = item.founding_date.strftime('%Y-%m-%d')
        dict['fund'] = item.registered_capital
        dict['fund_kind'] = item.registered_capital_currency
        dict['ind_code'] = item.industry_code
        if item.time_to_market != None:
            dict['ipo_time'] = item.time_to_market.strftime('%Y-%m-%d')
        dict['exchange'] = item.bourse
        if item.registered_province !=None:
            dict['reg_add'] = item.registered_province+"/"+item.registered_city+"/"+item.registered_district
        if item.actual_province != None:
            dict['real_add'] = item.actual_province+"/"+item.actual_city+"/"+item.actual_district
        dict['c_time'] = item.create_time.strftime('%Y-%m-%d %H:%M:%S')
        list.append(dict)

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

#用于向企业用户返回企业数据详细值
@login_required
def get_ent_detail(request,id):
    ent_info = EnterpriseInfo.objects.get(id=id)

    basic_name = ent_info.enterprise_name
    basic_code = ent_info.enterprise_id

    id = id


    c_time = ent_info.create_time.strftime('%Y-%m-%d %H:%M:%S')

    if ent_info.founding_date != None:
        date = ent_info.founding_date.strftime('%Y-%m-%d ')
    basic_fund = ent_info.registered_capital
    basic_fund_kind = ent_info.registered_capital_currency
    basic_ind = ent_info.industry
    basic_ind_code = ent_info.industry_code
    if ent_info.time_to_market != None:
        basic_IPO_time = ent_info.time_to_market.strftime('%Y-%m-%d ')
    basic_exchange = ent_info.bourse
    basic_reg_pro = ent_info.registered_province
    basic_reg_city = ent_info.registered_city
    basic_reg_area = ent_info.registered_district
    basic_real_pro = ent_info.actual_province
    basic_real_city = ent_info.actual_city
    basic_real_area = ent_info.actual_district

    ser_field = ent_info.service_field

    peo_count1 = ent_info.head_count
    peo_count2 = ent_info.above_bs_head_count

    ##财务信息暂时空着
    debt = 0
    equity = 0
    net_worth = 0
    grate_total = 0
    grate_bus = 0
    tax = 0

    ip_total = ent_info.applicated_patent_count
    ap_total = ent_info.ipc_top10_patent_count
    jp_total = ent_info.multi_applicated_patent_count_this_year
    sp_total = ent_info.sc_count
    ns_total = ent_info.standard_count

    inforplat_total = ent_info.informalization_platform_count
    icp_total = ent_info.icp_count

    honor_total = ent_info.honor_count
    a_taxpayer = ent_info.a_class_honor
    if ent_info.a_class_honor == 1:
        a_taxpayer = "是"
    else:
        a_taxpayer = "否"
    dishonesty = ent_info.dishonest_in_3_years
    if ent_info.dishonest_in_3_years ==1:
        dishonesty = "是"
    else:
        dishonesty = "否"
    lawsuit_total = ent_info.civil_action_count
    is_ep = ent_info.environmental_punishment_count
    if is_ep :
        is_ep = "是"
    else:
        is_ep = "否"

    invest_time = ent_info.investment_count
    invest_amount = ent_info.investment_amount
    bidding_time = 0
    bidding_amount = 0


    del ent_info

    for item in locals():
        print(item)
    '''
    for item in locals():
        if item.value == None:
            print("here")
            item.value = "空，未填写！"
        else:
            print(item)
'''
    return render(request,"data_handler/ent_data_detail.html",locals())

#用于向企业用户返回搜索后的企业数据
@login_required
def search_ent_info(request):
    print("here")
    params = request.POST.get('searchParams')
    print(params)
    params = json.loads(params)
    q = Q()
    id = params['id']
    if(id!=''):
        q = q&Q(id__contains=id)
    basic_name = params['basic_name']
    if (basic_name != ''):
        q = q & Q(enterprise_name__contains=basic_name)
    basic_id = params['basic_id']
    if (basic_id != ''):
        q = q & Q(enterprise_id__contains=basic_id)
    basic_reg_pro = params['basic_reg_pro']
    if (basic_reg_pro != ''and basic_reg_pro != None):
        q = q & Q(registered_province__contains=basic_reg_pro)
    basic_reg_city = params['basic_reg_city']
    if (basic_reg_city != '' and basic_reg_city != None):
        q = q & Q(registered_city__contains=basic_reg_city)
    basic_reg_area = params['basic_reg_area']
    if (basic_reg_area != '' and basic_reg_area != None):
        q = q & Q(registered_district__contains=basic_reg_area)
    basic_real_pro = params['basic_real_pro']
    if (basic_real_pro != '' and basic_real_pro != None):
        q = q & Q(actual_province__contains=basic_real_pro)
    basic_real_city = params['basic_real_city']
    if (basic_real_city != '' and basic_real_city != None):
        q = q & Q(actual_city__contains=basic_real_city)
    basic_real_area = params['basic_real_area']
    if (basic_real_area != '' and basic_real_area != None):
        q = q & Q(actual_district__contains=basic_real_area)

  #  q = Q(name__contains=name)&Q(email__contains=email)&Q(mobile__contains=mobile)&Q(type__contains=type)

    data = EnterpriseInfo.objects.filter(q,needpre=0)
    dataCount = data.count()
    pageIndex = request.POST.get('pageIndex')
    pageSize = request.POST.get('pageSize')

    list = []
    res = []
    for item in data:
        dict = {}
        dict['t_id'] = item.id
        dict['name'] = item.enterprise_name
        dict['id'] = item.enterprise_id
        if item.founding_date != None:
            dict['c_date'] = item.founding_date.strftime('%Y-%m-%d')
        dict['fund'] = item.registered_capital
        dict['fund_kind'] = item.registered_capital_currency
        dict['ind_code'] = item.industry_code
        if item.time_to_market != None:
            dict['ipo_time'] = item.time_to_market.strftime('%Y-%m-%d')
        dict['exchange'] = item.bourse
        if item.registered_province != None:
            dict['reg_add'] = item.registered_province + "/" + item.registered_city + "/" + item.registered_district
        if item.actual_province != None:
            dict['real_add'] = item.actual_province + "/" + item.actual_city + "/" + item.actual_district
        dict['c_time'] = item.create_time.strftime('%Y-%m-%d %H:%M:%S')
        list.append(dict)

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

#用于向企业用户返回搜索后的全部企业数据
@login_required
def search_ent_info_all(request):
    print("here")
    params = request.POST.get('searchParams')
    print(params)
    params = json.loads(params)
    q = Q()
    id = params['id']
    if(id!=''):
        q = q&Q(id__contains=id)
    basic_name = params['basic_name']
    if (basic_name != ''):
        q = q & Q(enterprise_name__contains=basic_name)
    basic_id = params['basic_id']
    if (basic_id != ''):
        q = q & Q(enterprise_id__contains=basic_id)
    basic_reg_pro = params['basic_reg_pro']
    if (basic_reg_pro != ''and basic_reg_pro != None):
        q = q & Q(registered_province__contains=basic_reg_pro)
    basic_reg_city = params['basic_reg_city']
    if (basic_reg_city != '' and basic_reg_city != None):
        q = q & Q(registered_city__contains=basic_reg_city)
    basic_reg_area = params['basic_reg_area']
    if (basic_reg_area != '' and basic_reg_area != None):
        q = q & Q(registered_district__contains=basic_reg_area)
    basic_real_pro = params['basic_real_pro']
    if (basic_real_pro != '' and basic_real_pro != None):
        q = q & Q(actual_province__contains=basic_real_pro)
    basic_real_city = params['basic_real_city']
    if (basic_real_city != '' and basic_real_city != None):
        q = q & Q(actual_city__contains=basic_real_city)
    basic_real_area = params['basic_real_area']
    if (basic_real_area != '' and basic_real_area != None):
        q = q & Q(actual_district__contains=basic_real_area)

  #  q = Q(name__contains=name)&Q(email__contains=email)&Q(mobile__contains=mobile)&Q(type__contains=type)

    data = EnterpriseInfo.objects.filter(q)
    dataCount = data.count()
    pageIndex = request.POST.get('pageIndex')
    pageSize = request.POST.get('pageSize')

    list = []
    res = []
    for item in data:
        dict = {}
        dict['t_id'] = item.id
        dict['name'] = item.enterprise_name
        dict['id'] = item.enterprise_id
        if item.founding_date != None:
            dict['c_date'] = item.founding_date.strftime('%Y-%m-%d')
        dict['fund'] = item.registered_capital
        dict['fund_kind'] = item.registered_capital_currency
        dict['ind_code'] = item.industry_code
        if item.time_to_market != None:
            dict['ipo_time'] = item.time_to_market.strftime('%Y-%m-%d')
        dict['exchange'] = item.bourse
        if item.registered_province != None:
            dict['reg_add'] = item.registered_province + "/" + item.registered_city + "/" + item.registered_district
        if item.actual_province != None:
            dict['real_add'] = item.actual_province + "/" + item.actual_city + "/" + item.actual_district
        dict['c_time'] = item.create_time.strftime('%Y-%m-%d %H:%M:%S')
        list.append(dict)

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

#用于向企业用户删除选中的企业数据
@login_required
def delete_ent_info(request):
    get_id = request.GET.get('id')
    EnterpriseInfo.objects.filter(id=get_id).delete()
    return HttpResponse('nice')

#用于向企业用户返回数据预处理页面的函数
@login_required
def get_ent_process(request):
    return render(request,"data_handler/ent_data_process.html")

#用于向企业用户数据预处理界面返回数据的函数
@login_required
def get_ent_pre_data(request):
    user = request.user
    myuser = Myuser.objects.get(u=user)
    data = EnterpriseInfo.objects.filter(mu=myuser)
    dataCount = data.count()
    pageIndex = request.POST.get('pageIndex')
    pageSize = request.POST.get('pageSize')

    list = []
    res = []
    for item in data:
        if item.needpre:
            dict = {}
            dict['t_id'] = item.id
            dict['name'] = item.enterprise_name
            dict['id'] = item.enterprise_id
            if item.founding_date != None:
                dict['c_date'] = item.founding_date.strftime('%Y-%m-%d')
            dict['fund'] = item.registered_capital
            dict['fund_kind'] = item.registered_capital_currency
            dict['ind_code'] = item.industry_code
            if item.time_to_market != None:
                dict['ipo_time'] = item.time_to_market.strftime('%Y-%m-%d')
            dict['exchange'] = item.bourse
            if item.registered_province !=None:
                dict['reg_add'] = item.registered_province+"/"+item.registered_city+"/"+item.registered_district
            if item.actual_province != None:
                dict['real_add'] = item.actual_province+"/"+item.actual_city+"/"+item.actual_district
            dict['c_time'] = item.create_time.strftime('%Y-%m-%d %H:%M:%S')
            list.append(dict)
        else:
            continue
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

#用于对缺失数据进行预处理的函数
@login_required
def ent_process_data(request):
    #此次应为
    #origindata = EnterpriseInfo.objects.filter(needpre=0)
    origindata = EnterpriseInfo.objects.all()
    data = []
    for item in origindata:
        data.append(item.getNumberAttr())
    rawdata = []
    params = request.POST.get('searchParams')
    type = request.POST.get("type")
    print(type)
    params = json.loads(params)
    len = 0
    for param in params:
        tempid = param['t_id']
        print(tempid)
        tempinfo = EnterpriseInfo.objects.get(id=tempid)
        rawdata.append(tempinfo)
        data.append(tempinfo.getNumberAttr())
        len +=1

    print(data)

    if len != 10:
        data = pd.DataFrame(data)
        if type == "GAIN":
            params = PreParams.objects.filter(type=type).latest('id')
            #print(params)
            data = GAIN(data,params)
        elif type == "VAEGAIN":
            data = VAE_GAIN(data)
        elif type == "SCIS":
            params = PreParams.objects.filter(type=type).latest('id')
            data = SCIS(data,params)

        results = data.tolist()
        results = results[-len:]
        for i in range(len):
            rawdata[i].setNumberAttr(results[i])

            rawdata[i].needpre = 0
            rawdata[i].save()

    return get_ent_pre_data(request)

#用于提供修改预处理算法参数页面的函数
@login_required
def admin_get_preparams(request):
    scis = PreParams.objects.filter(type="SCIS").latest('id')
    gain = PreParams.objects.filter(type="GAIN").latest('id')

    return render(request,"data_handler/admin_pre_params.html",locals())

#用于修改预处理算法参数的函数
@login_required
def admin_update_preparams(request):
    print("test")
    temp_scis = PreParams()
    temp_gain = PreParams()
    temp_scis.type = "SCIS"
    temp_gain.type = "GAIN"
    try:
        temp_scis.batch_size = request.POST.get("scis_bs")
        temp_scis.hint_rate = request.POST.get("scis_hr")
        temp_scis.alpha = request.POST.get("scis_al")
        temp_scis.iterations = request.POST.get("scis_iter")
        temp_scis.epoch = request.POST.get("scis_ep")
        temp_scis.guarantee = request.POST.get("scis_gu")
        temp_scis.thre_value = request.POST.get("scis_tv")
        temp_scis.initial_value = request.POST.get("scis_iv")
        temp_scis.epsilon = request.POST.get("scis_eps")
        temp_scis.value = request.POST.get("scis_va")
        temp_scis.s_miss = request.POST.get("scis_sm")

        temp_gain.batch_size = request.POST.get("gain_bs")
        temp_gain.hint_rate = request.POST.get("gain_hr")
        temp_gain.alpha = request.POST.get("gain_al")
        temp_gain.iterations = request.POST.get("gain_iter")
        temp_gain.epoch = request.POST.get("gain_ep")
        temp_gain.guarantee = request.POST.get("gain_gu")
        temp_gain.thre_value = request.POST.get("gain_tv")
        temp_gain.initial_value = request.POST.get("gain_iv")
        temp_gain.epsilon = request.POST.get("gain_eps")
        temp_gain.value = request.POST.get("gain_va")
        temp_gain.s_miss = request.POST.get("gain_sm")

        now = datetime.now(pytz.timezone('Asia/Shanghai'))
        format_time = now.strftime('%Y-%m-%d %H:%M:%S')
        temp_scis.create_time = format_time
        temp_gain.create_time = format_time
        temp_scis.save()
        temp_gain.save()
        messages.add_message(request, messages.SUCCESS, '修改成功！')

    except Exception as e :
        messages.add_message(request,messages.ERROR,str(e))


    return redirect("/admin/pre_params")

#用于提供企业数据下载页面的函数
@login_required
def ent_data_download(request):
    return render(request,"data_handler/ent_data_download.html")

#用于提供下载单个企业数据的函数
@login_required
def ent_download_singledata(request,id):
    get_id = id
    info = EnterpriseInfo.objects.filter(id=get_id).values()
    print(type(info))
    df = pd.DataFrame.from_records(info)
    del df['registered_street']
    del df['actual_street']
    del df['mu_id']
    del df['needpre']
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    format_time = now.strftime('%Y-%m-%d %H:%M:%S')
    filename = f"{get_id}_企业数据_{format_time}.csv"
    response = HttpResponse(content_type='text/csv')
    response = HttpResponse(content_type='text/csv')  # 定义一个HttpResponse，类型是csv
    response.charset = 'utf-8-sig' if "Windows" in request.headers.get('User-Agent') else 'utf-8'
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    df.to_csv(path_or_buf=response, index=False,encoding="utf_8")
    return response

#用于提供下载多个企业数据的函数
@login_required
def ent_download_data(request):
    ids = request.POST.get("ids")
    ids = json.loads(ids)
    result = EnterpriseInfo.objects.filter(id=-1)
    for id in ids:
        print(id['id'])
        print(type(id))
        info = EnterpriseInfo.objects.filter(id=id['t_id'])
        print(info[0].enterprise_id)
        result = info | result
    df = pd.DataFrame.from_records(result.values())
    print(df)
    del df['registered_street']
    del df['actual_street']
    del df['mu_id']
    del df['needpre']
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    format_time = now.strftime('%Y-%m-%d %H:%M:%S')
    filename = f"企业数据_{format_time}.csv"
    response = HttpResponse(content_type='text/csv')  # 定义一个HttpResponse，类型是csv
    response.charset = 'utf-8-sig' if "Windows" in request.headers.get('User-Agent') else 'utf-8'
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    df.to_csv(path_or_buf=response, index=False, encoding="utf_8")
    return response

#用于测试process类
def ent_generate_process(request):
    user = request.user
    mu = Myuser.objects.get(u=user)
    ids = request.POST.get("ids")
    ids = json.loads(ids)
    status = "已添加数据，请选择指标"
    temptype = 1
    if len(ids)>1 :
        temptype = 2

    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    format_time = now.strftime('%Y-%m-%d %H:%M:%S')
    create_time = format_time
    update_time = format_time

    temppro = Process.objects.create(mu = mu, status = status , create_time = create_time, update_time = update_time, type = temptype)

    for id in ids:
        tempinfo = EnterpriseInfo.objects.get(id=id['t_id'])
        temppro.ent_info.add(tempinfo)

    '''
    temppro.mu = mu
    temppro.status = "已添加数据，请选择指标"
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    format_time = now.strftime('%Y-%m-%d %H:%M:%S')
    temppro.create_time = format_time
    temppro.update_time = format_time
    '''

    temppro.save()

    messages.add_message(request, messages.SUCCESS, "上传成功！")

    return render(request,"data_handler/ent_data_search.html")