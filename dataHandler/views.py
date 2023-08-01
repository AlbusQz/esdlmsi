from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
#测试函数
@login_required
def ent_upload_data(request):
    return render(request,'data_handler/ent_data_upload.html')