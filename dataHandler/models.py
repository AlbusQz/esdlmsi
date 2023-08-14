# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from myUser.models import Myuser

class EnterpriseInfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    enterprise_id = models.IntegerField(null=False)
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

    class Meta:
        managed = False
        db_table = 'enterprise_info'
        unique_together = (('enterprise_id', 'mu'),)
