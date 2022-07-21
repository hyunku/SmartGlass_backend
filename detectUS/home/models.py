from csv import unregister_dialect
from django.db import models
from django.conf import settings
from django.utils import timezone

class account(models.Model):
    user_id = models.CharField(max_length=45,null=False,primary_key=True)
    user_pw = models.CharField(max_length=20,null=False)
    company_id = models.ForeignKey('listapp.Company', on_delete=models.CASCADE,default='',db_column='company_id')
    is_admin = models.IntegerField(null=False,default='0')# 
    name = models.CharField(max_length=45,null=False,default='')

    class Meta:
        db_table = 'account'


class glass(models.Model):
    glass_id = models.AutoField(null=False,primary_key=True)
    glass_name = models.CharField(max_length=45,null=False)
    # user_id foreign key
    # building_id foreing key

    class Meta:
        db_table = 'glass'


class raw_data(models.Model):
    raw_data_id = models.AutoField(null=False,primary_key=True)
    picture = models.CharField(max_length=100,null=True)
    voice = models.CharField(max_length=100,null=True)
    voice_to_text = models.CharField(max_length=100,null=True)
    upload_user_id = models.CharField(max_length=45,null=True)
    upload_target_building = models.IntegerField(null=True)

    class Meta:
        db_table = 'raw_data'


    
