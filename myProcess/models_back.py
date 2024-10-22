from django.db import models
from datetime import datetime
import pandas as pd
from django.db import models
from myUser.models import Myuser
from dataHandler.models import EnterpriseInfo
# Create your models here.

class Process(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    mu = models.OneToOneField(Myuser, on_delete=models.CASCADE)
    type = models.IntegerField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    status = models.CharField(max_length=255, db_collation='utf8_general_ci')
    index = models.IntegerField(blank=True, null=True)
    report = models.IntegerField(blank=True, null=True)
    ent_info = models.ManyToManyField(to=EnterpriseInfo,db_table="pro_entinfo")

    class Meta:
        managed = False
        db_table = 'process'
