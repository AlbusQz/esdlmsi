from django.shortcuts import render
from django.http import HttpResponse
from .models import Users

# Create your views here.

def testloginpage(request):
    users = Users.objects.all()
    user_list = list()
    for count,user in enumerate(users):
