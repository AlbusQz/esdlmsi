# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import datetime
import pandas as pd
from django.db import models
from myUser.models import Myuser
import numpy as np

class EnterpriseInfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.

    enterprise_id = models.CharField(max_length=64, blank=True, null=False)
    enterprise_name = models.CharField(max_length=64, blank=True, null=True)
    founding_date = models.DateField(blank=True, null=True)
    registered_capital = models.IntegerField(blank=True, null=True)
    registered_capital_currency = models.CharField(max_length=64, blank=True, null=True)
    registered_province = models.CharField(max_length=64, blank=True, null=True)
    registered_city = models.CharField(max_length=64, blank=True, null=True)
    registered_district = models.CharField(max_length=64, blank=True, null=True)
    registered_street = models.CharField(max_length=64, blank=True, null=True)
    actual_province = models.CharField(max_length=64, blank=True, null=True)
    actual_city = models.CharField(max_length=64, blank=True, null=True)
    actual_district = models.CharField(max_length=64, blank=True, null=True)
    actual_street = models.CharField(max_length=64, blank=True, null=True)
    industry = models.CharField(max_length=64, blank=True, null=True)
    industry_code = models.CharField(max_length=64, blank=True, null=True)
    time_to_market = models.DateField(blank=True, null=True)
    bourse = models.CharField(max_length=64, blank=True, null=True)

    service_field = models.CharField(max_length=64, blank=True, null=True)

    head_count = models.IntegerField(blank=True, null=True)
    above_bs_head_count = models.IntegerField(blank=True, null=True)

    applicated_patent_count = models.PositiveIntegerField(blank=True, null=True)
    ipc_top10_patent_count = models.PositiveIntegerField(db_column='IPC_top10_patent_count', blank=True, null=True)  # Field name made lowercase.
    multi_applicated_patent_count_this_year = models.PositiveIntegerField(blank=True, null=True)
    sc_count = models.PositiveIntegerField(blank=True, null=True)
    standard_count = models.PositiveIntegerField(blank=True, null=True)

    informalization_platform_count = models.PositiveIntegerField(blank=True, null=True)
    icp_count = models.PositiveIntegerField(db_column='ICP_count', blank=True, null=True)  # Field name made lowercase.

    honor_count = models.IntegerField(blank=True, null=True)
    a_class_honor = models.IntegerField(db_column='A_class_honor', blank=True, null=True)  # Field name made lowercase.
    dishonest_in_3_years = models.IntegerField(blank=True, null=True)
    civil_action_count = models.PositiveIntegerField(blank=True, null=True)
    environmental_punishment_count = models.PositiveIntegerField(blank=True, null=True)


    investment_count = models.PositiveIntegerField(blank=True, null=True)
    investment_amount = models.PositiveIntegerField(blank=True, null=True)

    create_time = models.DateTimeField(blank=True, null=True)
    mu = models.OneToOneField(Myuser, on_delete=models.CASCADE)

    needpre = models.PositiveIntegerField(blank=True, null=True)

    #用来判断上传数据是否符合要求的函数
    @staticmethod
    def isValid(input):
        def check_time_format(time_str):
            if time_str == None or str(time_str) == "nan":
                return True
            try:
                datetime.strptime(time_str, '%Y-%m-%d')
                return True
            except ValueError:
                return False
        types = [str, int, str, float,str,
                 str, float, str,str,
                  str, str, str,

                 str, str, str,

                  str, float, float,
                 float, float, float, float,
                 float, float, float, float,
                 float, float, float, float,
                 float, float]
        titles = ["enterprise_name","enterprise_id","founding_date","registered_capital", "registered_capital_currency",
                  "industry", "industry_code", "time_to_market","bourse",
                 "registered_province","registered_city","registered_district",

                  "actual_province","actual_city","actual_district",

                  "service_field","head_count","above_bs_head_count","applicated_patent_count","IPC_top10_patent_count","multi_applicated_patent_count_this_year","sc_count","standard_count","informalization_platform_count","ICP_count","honor_count","A_class_honor","dishonest_in_3_years","civil_action_count","environmental_punishment_count","investment_count","investment_amount"]

        if(len(input)!=len(types)):
            return False,"上传文件的数据项长度不同！"

        temp1 = ''
        for i in range(len(input)):
            if input[i] is not None:
                if(type(input[i])!=types[i] and str(input[i])!="nan"):
                    if (type(input[i])==int and types[i]==float) or(type(input[i])==pd._libs.tslibs.timestamps.Timestamp and types[i]==str):
                        continue
                    else:
                        temp1 +=titles[i]+"列数据格式不匹配！\n"

                        print(i)
                        #print(i == )
                        print(input[i])
                        print(titles[i])
                        print(input[i])
                        print((types[i]))
                        print(type(input[i]))

        if(temp1 != ''):
            return False,temp1

        if(input[1] is None or str(input[1])=="nan" ):
            return False,"数据必填项"+titles[1]+"为空！"

        if str(input[2])=="nan":
            input[2] = None
        if str(input[7]) == "nan":
            input[7] = None
        if(check_time_format(input[2])==False or check_time_format(input[7])==False ):
            print(input[2])
            return False, "时间项格式错误！"

        print("here")
        return True,"nice!111"

    #用来处理上传数据的函数
    def setAll(self,input):
        print(input[0])

        self.setBasic(input[0:15])
        self.setScope(input[15])
        self.setPeople(input[16],input[17])
        self.setPatent(input[18:23])
        self.setInfromation(input[23],input[24])
        self.setHonor(input[25:30])
        self.setInvest(input[30],input[31],0,0)


    #用来初始化基础信息模块数据的函数
    def setBasic(self,enterprise_name, enterprise_id, founding_date, registered_capital,
                   registered_capital_currency, industry, industry_code, time_to_market,
                   bourse, registered_province,registered_city, registered_district,
                   actual_province, actual_city, actual_district):
        self.enterprise_name =enterprise_name
        self.enterprise_id = enterprise_id
        if founding_date != '':
            self.founding_date = founding_date
        self.registered_capital = registered_capital
        self.registered_capital_currency = registered_capital_currency
        self.industry = industry
        self.industry_code = industry_code
        if time_to_market !='':
            self.time_to_market = time_to_market
        self.bourse = bourse
        self.registered_province = registered_province
        self.registered_city = registered_city
        self.registered_district = registered_district
        self.actual_province = actual_province
        self.actual_city = actual_city
        self.actual_district = actual_district

    def setBasic(self,plist):
        self.enterprise_name = plist[0]
        self.enterprise_id = plist[1]
        if plist[2]!='':
            self.founding_date = plist[2]
        self.registered_capital = plist[3]
        self.registered_capital_currency = plist[4]
        self.industry = plist[5]
        self.industry_code = plist[6]
        if plist[7]!='':
            self.time_to_market = plist[7]
        self.bourse = plist[8]
        self.registered_province = plist[9]
        self.registered_city = plist[10]
        self.registered_district = plist[11]
        self.actual_province = plist[12]
        self.actual_city = plist[13]
        self.actual_district = plist[14]


    # 用来初始化经营范围模块数据的函数
    def setScope(self,service_fild):
        self.service_field = service_fild

    # 用来初始化人才结构模块数据的函数
    def setPeople(self,head_count,above_bs_head_count):
        self.head_count = head_count
        self.above_bs_head_count = above_bs_head_count

    # 用来初始化财务信息模块数据的函数(有待实现)
    def setFinance(self,):
        return

    # 用来初始化专利/知识产权模块数据的函数
    def setPatent(self,applicated_patent_count, ipc_top10_patent_count,
                  multi_applicated_patent_count_this_year, sc_count, standard_count ):
        self.applicated_patent_count = applicated_patent_count
        self.ipc_top10_patent_count = ipc_top10_patent_count
        self.multi_applicated_patent_count_this_year = multi_applicated_patent_count_this_year
        self.sc_count = sc_count
        self.standard_count = standard_count

    def setPatent(self,plist):
        self.applicated_patent_count = plist[0]
        self.ipc_top10_patent_count = plist[1]
        self.multi_applicated_patent_count_this_year = plist[2]
        self.sc_count = plist[3]
        self.standard_count = plist[4]

    # 用来初始化信息化建设模块数据的函数
    def setInfromation(self,informalization_platform_count, icp_count):
        self.informalization_platform_count = informalization_platform_count
        self.icp_count = icp_count

    # 用来初始化企业荣誉和信用模块数据的函数
    def setHonor(self,honor_count,a_class_honor, dishonest_in_3_years,
                 civil_action_count, environemntal_punishment_count):
        self.honor_count = honor_count
        self.a_class_honor = a_class_honor
        self.dishonest_in_3_years = dishonest_in_3_years
        self.civil_action_count = civil_action_count
        self.environmental_punishment_count = environemntal_punishment_count

    def setHonor(self,plist):
        self.honor_count = plist[0]
        self.a_class_honor = plist[1]
        self.dishonest_in_3_years = plist[2]
        self.civil_action_count = plist[3]
        self.environmental_punishment_count = plist[4]

    # 用来初始化对外投资和招投标模块数据的函数(待补充投标部分)
    def setInvest(self,investment_count,investment_amount,tender_count,tender_amount):
        self.investment_count = investment_count
        self.investment_amount = investment_amount

    #用于获得预处理算法中仅数值属性的函数
    def getNumberAttr(self):
        result = []
        result.append(self.head_count)
        result.append(self.above_bs_head_count)

        result.append(self.applicated_patent_count)
        result.append(self.ipc_top10_patent_count)
        result.append(self.multi_applicated_patent_count_this_year)
        result.append(self.sc_count)
        result.append(self.standard_count)

        result.append(self.informalization_platform_count)
        result.append(self.icp_count)

        result.append(self.honor_count)
        result.append(self.civil_action_count)

        result.append(self.investment_count)
        result.append(self.investment_amount)
        return result
    # 用于填补预处理算法中仅数值属性的函数
    def setNumberAttr(self,result):

        self.head_count = result[0]
        self.above_bs_head_count = result[1]

        self.applicated_patent_count = result[2]
        self.ipc_top10_patent_count = result[3]
        self.multi_applicated_patent_count_this_year = result[4]
        self.sc_count = result[5]
        self.standard_count = result[6]

        self.informalization_platform_count = result[7]
        self.icp_count = result[8]

        self.honor_count = result[9]
        self.civil_action_count = result[10]

        self.investment_count = result[11]
        self.investment_amount = result[12]

    #用于判断是否需要预处理的函数
    def getNeedpre(self):
        temp = self.getNumberAttr()
        for item in temp:
            #print("here")
            if item is None:
                return True
        return False
    class Meta:
        managed = False
        db_table = 'enterprise_info'
        unique_together = (('enterprise_id', 'mu'),)

#预处理算法的参数类
class PreParams(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=255)
    batch_size = models.IntegerField()
    hint_rate = models.FloatField()
    alpha = models.IntegerField()
    iterations = models.IntegerField()
    epoch = models.IntegerField()
    guarantee = models.FloatField()
    thre_value = models.FloatField()
    initial_value = models.IntegerField()
    epsilon = models.FloatField()
    value = models.IntegerField()
    s_miss = models.IntegerField()
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pre_params'

