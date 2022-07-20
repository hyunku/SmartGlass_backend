from curses import REPORT_MOUSE_POSITION
from tkinter import CASCADE
from django.db import models

# Create your models here.
class Issue(models.Model):
    issue_id=models.BigAutoField(null=False,primary_key=True)
#    raw_data_id=models.ForeignKey("Raw_data",on_delete=models.CASCADE, db_column='raw_data_id')
#    building_id=models.ForeignKey("Building",on_delete=models.CASCADE, db_column='building_id')
    floor=models.CharField(max_length=10,null=True)
    room=models.CharField(max_length=100,null=True)
    details=models.CharField(max_length=100,null=True)

    class Meta:
        db_table='issue'

class Floor(models.Model):
    floor=models.IntegerField(null=False)
#   building_id=models.ForeignKey("Building",on_delete=models.CASCADE, db_column='building_id')
    drawing_id =models.ForeignKey("Drawing",on_delete=models.CASCADE, db_column='drawing_id')
    class Meta:
        db_table='floor'
        
        
class Drawing(models.Model):
    drawing_id =models.BigAutoField(null=False,primary_key=True)
    drawing=models.CharField(max_length=100,null=False)
    class Meta:
        db_table='Drawing'
        