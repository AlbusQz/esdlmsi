# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class Myuser(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    password = models.CharField(max_length=16)
    type = models.CharField(max_length=5)
    name = models.CharField(max_length=16, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    mobile = models.IntegerField(unique=True, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    u = models.OneToOneField(User,on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'myuser'


class Test(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=7)
    mobile = models.CharField(unique=True, max_length=11)

    class Meta:
        #managed = False
        db_table = 'test'
