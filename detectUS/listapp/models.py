from django.db import models
from django.db.models import CASCADE


# Create your models here.
class Company(models.Model):
    company_id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=64) # 문자열 필드 (최대길이 : 64)

class Building(models.Model):
    company_id = models.ForeignKey(Company, on_delete=CASCADE, db_column='company_id') # 외래키 지정
    building_name = models.TextField(null=False) #null값 존재여부
    building_id = models.BigAutoField(primary_key=True)
    max_floor = models.IntegerField(null=True)
    min_floor = models.IntegerField(null=True)
    context = models.CharField(max_length=1024)

    class Meta:
        ordering = ['-max_floor'] # db정렬 방식 -> -붙으면 내림차순 (max_floor에 대한 내림차순 정렬)

