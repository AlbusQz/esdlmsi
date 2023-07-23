from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.apps import apps
from django.contrib.auth.hashers import make_password

# Create your models here.
class test(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    #password = models.CharField(max_length=16)
    type = models.CharField(max_length=7)
    mobile = models.CharField(max_length=11,unique=True,verbose_name="手机号")
    class Meta:
        #managed = False
        db_table = 'test'



'''
class myuser(AbstractUser):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    #email = models.EmailField(max_length=255,unique=True,verbose_name="电子邮箱",null=True)

    #username = models.CharField(max_length=255,unique=True,null=True)
    #password = models.CharField(max_length=16)
    #USERNAME_FIELD = 'email'
    ''''''
    TYPE_CHOICE = (
        ('管理员用户','管理员用户'),
        ('企业用户','企业用户'),
        ('政府用户', '政府用户'),
        ('行业专家用户', '行业专家用户')
    )
    type = models.CharField(max_length=8,choices=TYPE_CHOICE)
    mobile = models.CharField(max_length=11,unique=True,verbose_name="手机号",null=True)
    create_time = models.TimeField(auto_now_add=True)
    update_time = models.TimeField(null=True)

    objects = UserManager()

    class Meta:
        db_table = 'myUser'
'''