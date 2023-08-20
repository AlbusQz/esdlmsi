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