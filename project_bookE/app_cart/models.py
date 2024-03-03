from django.db import models
from app_user.models import *
from app_store.models import *

# Create your models here.

class Shoppingcart(models.Model):
    id = models.AutoField(db_column='ID_cart', primary_key=True)  # Field name made lowercase.
    customerid = models.OneToOneField(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.
   
    # class Meta:
        
    #     db_table = 'shoppingcart'
    
    @property
    def total(self):
        s = 0
        for cartline in Cartline.objects.filter(shoppingcartid__id = self.id, is_active = True):
            s += cartline.sumPrice
        return s
  
    
    


class Cartline(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_product = models.ForeignKey(Book, models.CASCADE, db_column='ID_book')  # Field name made lowercase.
    num = models.IntegerField(db_column='Num', blank=True, null=True)  # Field name made lowercase.
    shoppingcartid = models.ForeignKey(Shoppingcart, models.CASCADE, db_column='ShoppingCartID')  # Field name made lowercase.
    is_order  = models.BooleanField(null=True, default= False)
    is_active  = models.BooleanField(null=True, default= True)
    is_selected = models.BooleanField(null=True, default= False)
    # class Meta:
        
    #     db_table = 'cartline'


    @property
    def sumPrice(self):
        return (self.num * self.id_product.price)
