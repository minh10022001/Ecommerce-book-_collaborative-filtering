

from django.db import models
from app_account.models import Account

class Staff(Account):
  
    phone_number = models.CharField(max_length=50)
    date_created = models.DateField(default=None, null=True)
    dob = models.DateField(default=None, null=True)
    gender = models.CharField(max_length=50, null=True)
    start_date =  models.DateField(default=None, null=True)
    position = models.CharField(max_length=50, null=True)
    salary = models.FloatField(null= True)
    note =  models.CharField(max_length=1000, null= True)

    class Meta:
        app_label = 'app_staff'

class OrderHistoryLog(models.Model):
    id_order =  models.IntegerField(null= True)
    status_current =  models.CharField(max_length=1000, null= True)
    action_by_type_user = models.CharField(max_length=1000, null= True)
    id_user = models.IntegerField(null= True)
    date_modifided = models.DateField(default=None, null=True)
    id_staff =  models.ForeignKey(Staff, db_column='ID_staff', on_delete=models.SET_NULL, null= True)
    class Meta:
        app_label = 'app_staff'

