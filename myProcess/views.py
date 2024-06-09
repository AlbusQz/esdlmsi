import pytz
from django.core.paginator import Paginator
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse,Http404
import pandas as pd
from myUser.models import Myuser
from django.contrib import messages
from .models import EnterpriseInfo
import json
from django.db.models import Q
from dataHandler.VAEGAIN import VAE_GAIN
from dataHandler.SCIS import SCIS
from dataHandler.GAIN import GAIN
from myProcess.models import Process
from myUser.models import Myuser

#用于生成企业用户分析过程的函数
@login_required
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

#用于获得企业用户个人分析历史页面的函数
@login_required
def ent_get_processhistorypage(request):
    return render(request,"my_process/process_history.html")

#用于获得企业用户个人分析历史数据的函数
@login_required
def ent_get_processhis(request):
    user = request.user
    mu = Myuser.objects.get(u=user)
    data = Process.objects.filter(mu=mu)
    dataCount = data.count()
    pageIndex = request.POST.get('pageIndex')
    pageSize = request.POST.get('pageSize')

    list = []
    res = []
    for item in data:
        dict = {}
        dict['id'] = item.id
        if item.type == 1 :
            dict['type'] = "单个企业分析"
        else:
            dict['type'] = "多个企业分析"
        dict['c_time'] = item.create_time.strftime('%Y-%m-%d %H:%M:%S')
        dict['u_time'] = item.update_time.strftime('%Y-%m-%d %H:%M:%S')
        dict['status'] = item.status
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

#用于搜索企业用户个人分析历史数据的函数
@login_required
def ent_search_processhis(request):
    #print("here")
    params = request.POST.get('searchParams')
    #print(params)
    params = json.loads(params)
    q = Q()
    id = params['id']
    if (id != ''):
        q = q & Q(id__contains=id)
    type = params['type']
    #print(type)
    if (type != '' and type !='0' and type !=0):
        #print("here")
        q = q & Q(type__contains=type)
    status = params['status']
    if (status != ''):
        q = q & Q(status__contains=status)


    #  q = Q(name__contains=name)&Q(email__contains=email)&Q(mobile__contains=mobile)&Q(type__contains=type)

    data = Process.objects.filter(q)
    dataCount = data.count()
    pageIndex = request.POST.get('pageIndex')
    pageSize = request.POST.get('pageSize')

    list = []
    res = []
    for item in data:
        dict = {}
        dict['id'] = item.id
        if item.type == 1:
            dict['type'] = "单个企业分析"
        else:
            dict['type'] = "多个企业分析"
        dict['c_time'] = item.create_time.strftime('%Y-%m-%d %H:%M:%S')
        dict['u_time'] = item.update_time.strftime('%Y-%m-%d %H:%M:%S')
        dict['status'] = item.status
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

#用于向企业用户删除选中的处理过程数据的函数
@login_required
def delete_ent_process_his(request):
    get_id = request.POST.get('id')
    Process.objects.filter(id=get_id).delete()
    return HttpResponse('nice')

#用于向企业用户返回处理过程详细信息的函数
@login_required
def get_ent_process_detail(request,id):
    process = Process.objects.get(id=id)
    id = process.id
    type = process.type
    status = process.status
    c_time = process.create_time.strftime('%Y-%m-%d %H:%M:%S')
    u_time = process.update_time.strftime('%Y-%m-%d %H:%M:%S')

    del process

    return render(request,"my_process/ent_processhis_detail.html",locals())

#用于获得处理过程所包含数据信息的函数
@login_required
def get_ent_processhis_data(request,id):
    print("test")
    print(id)
    process = Process.objects.get(id=id)
    data = process.ent_info.all()

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

#用于返回临时指标选择页面的函数
@login_required
def temp_get_select(request):
    return render(request,"select_index.html")

#用于返回临时404页面的函数
@login_required
def temp_404(request):
    return render(request,"404_2.html")

