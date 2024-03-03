
from django.db import models
from app_store.models import *
from app_cart.models import *
from  app_user.models import *
from app_cart.models import Shoppingcart
from datetime import datetime
# Create your models here.


class Shipping(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    address = models.ForeignKey(AddressShipping, models.CASCADE, db_column='addressID')  # Field name made lowercase.
    method= models.CharField(db_column='ShippingMethod', max_length=255, blank=True, null=True)
    date_shipping = models.DateField(db_column='DateShipping', blank=True, null=True) 
    delayshipnote = models.CharField(db_column='DelayShipNote', max_length=255, blank=True, null=True)
    price_shipping = models.FloatField(null= True)

class Payment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    isComplete = models.BooleanField(blank=True, null=True, default = True)
    method = models.CharField(db_column='Method', max_length=255, blank=True, null=True)  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True) 
    id_cart = models.ForeignKey(Shoppingcart, models.CASCADE, db_column='IDcart')  # Field name made lowercase.
    id_shipping =  models.ForeignKey(Shipping, models.CASCADE, db_column='IDshipping')
    amount = models.FloatField(null= True)

    def __str__(self):
        return self.method

class Order(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    paymentid = models.OneToOneField('Payment', models.CASCADE, db_column='PaymentID')  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.
    shippingid = models.ForeignKey(Shipping, models.CASCADE, db_column='ShippingID',blank=True, null=True)
    cartid = models.ForeignKey(Shoppingcart, models.CASCADE, db_column='CartID',blank=True, null=True)
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=255, blank=True, null=True)  # Field name made lowercase.
    
    @property
    def cost_all_items(self):
        sum = 0
        for orderitem in Orderitem.objects.filter(orderid__id = self.id):
            sum += orderitem.subTotal
        return sum
    # @property
    # def cost_shipping(self):
    #     costship = 0
    #     if self.cost_all_items >= 500000:
    #         costship  = 0
    #     else:
    #         if self.shippingmethod =='Giao hàng nhanh':
    #             costship  = 20000
    #         elif self.shippingmethod =='Giao hàng tiêu chuẩn':
    #             costship =  10000
    #     return costship
    # @property
    # def total(self):
    #     sum = self.cost_all_items+ self.cost_shipping
    #     return sum



class Orderitem(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    orderid = models.ForeignKey(Order, models.CASCADE, db_column='OrderID')  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey(Book, models.CASCADE, db_column='ItemID')  # Field name made lowercase.
    cartline =  models.OneToOneField(Cartline,models.CASCADE,db_column='CartlineID', null=True)

    @property
    def exact_price(self):
        order =  Order.objects.get(id =  self.orderid.id)
        importbooks =  ImportBook.objects.filter(id_product = self.product)
        
        lastest_import = None
        min_diff  = 10e9
        for im in importbooks:
            # ngay_order_obj = datetime.strptime(str(order.time), "%Y-%m-%d")
            # ngay_import_obj = datetime.strptime(str(im.create_at), "%Y-%m-%d")
            # diff = ngay_order_obj - ngay_import_obj
            diff =  order.time -  im.create_at
            diff = diff.days
            if diff < min_diff:
                min_diff = diff
                lastest_import = im
            elif diff == min_diff:
                if lastest_import.is_sale ==True:
                    lastest_import = lastest_import
                    min_diff =  diff
                elif im.is_sale == True:
                    lastest_import = im
            else:
                pass
        return im.price_sale

    @property
    def subTotal(self):
        return self.count*self.exact_price

