# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    #password = models.CharField(max_length=16)
    type = models.CharField(max_length=7)
    mobile = models.CharField(max_length=11,unique=True,verbose_name="手机号")
    class Meta:
        managed = False
        db_table = 'users'
