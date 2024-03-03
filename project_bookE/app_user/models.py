# Create your models here.
from cgi import test
from django.db import models
from app_account.models import Account


class Customer(Account):
    phone_number = models.CharField(max_length=50)
    date_created = models.DateField(default=None, null=True)
    dob = models.DateField(default=None, null=True)
    gender = models.CharField(max_length=50, null=True)
   
    class Meta:
        app_label = 'app_user'
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin    # Admin có tất cả quyền trong hệ thống

    def has_module_perms(self, add_label):
        return True

    def full_name(self):
        return self.fullname

class AddressShipping(models.Model):
    name_receiver = models.CharField(max_length=50, null= True)
    receiver_phone = models.CharField(max_length=50, null= True)
    city = models.CharField(max_length=50, null= True)
    district = models.CharField(max_length=50, null= True)
    ward = models.CharField(max_length=50, null= True)
    address_detail = models.CharField(max_length=100, null= True)
    account = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    is_active =  models.BooleanField(null=True, default= True)

    def full_address(self):
        if self.address_detail is None:
            self.address_detail = ''
        else:
            self.address_detail = self.address_detail +","
        if self.ward is None:
            self.ward = ''
        else:
            self.ward = self.ward +','
        if self.district is None:
            self.district =''
        else:
            self.district =  self.district +','
        return self.address_detail  + self.ward  + self.district  +self.city
    def __str__(self):
        if self.address_detail is None:
            self.address_detail = ''
        else:
            self.address_detail = self.address_detail +","
        if self.ward is None:
            self.ward = ''
        else:
            self.ward = self.ward +','
        if self.district is None:
            self.district =''
        else:
            self.district =  self.district +','
        
        return self.address_detail  + self.ward + self.district  +self.city
