from distutils.command.upload import upload
from unicodedata import category
from django.db import models
from app_user.models import *
from django.urls import reverse


class Category(models.Model):
    id = models.IntegerField(db_column='ID_category', primary_key=True) 
    slug_category  = models.CharField(max_length=200, null= True)
    category_name  = models.CharField(max_length=200, null= True)

    def get_url(self):
        return reverse('products_by_category', args=[self.slug_category])

    
    

class Book(models.Model):
    id = models.IntegerField(db_column='ID_product', primary_key=True) 
    name  = models.CharField(max_length=500, null= True)
    price = models.FloatField(null= True)
    short_description = models.TextField( null= True)
    author = models.CharField(max_length=500, null= True)
    slug = models.CharField(max_length=500, null= True)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    is_authenic = models.CharField(max_length=500, null= True)
    publisher = models.CharField(max_length=500, null= True)
    publication_year = models.CharField(max_length=500, null= True)
    dimensions = models.CharField(max_length=1000, null= True)
    book_cover = models.CharField(max_length=500, null= True)
    numpage = models.CharField(max_length=500, null= True)
    manufacturer = models.CharField(max_length=500, null= True)
    image = models.ImageField(upload_to="download/",max_length = 500)
    stock = models.IntegerField(null= True) 
    count_review =  models.IntegerField(null= True) 
    avg_rating = models.FloatField(null= True)
    is_upload  = models.BooleanField(default= True, null= True)

    def __str__(self) -> str:
        return self.name

class Wishlistline(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  
    id_product = models.ForeignKey(Book, models.CASCADE, db_column='ID_product', blank=True, null=True)
    id_customer = models.ForeignKey(Customer, models.CASCADE, db_column='ID_customer', blank=True, null=True)
    create_at = models.DateField(null= True, default=None)  
  
class RatingBook(models.Model):
    id = models.IntegerField(db_column='ID_rating', primary_key=True) 
    content  = models.CharField(max_length=20000, null= True)
    id_customer= models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    id_product = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(null= True)
    create_at = models.DateField(null= True, default=None)

class ImportBook(models.Model):
    id =  models.IntegerField(db_column='ID_import', primary_key=True) 
    price_import = models.FloatField(null= True)
    price_sale = models.FloatField(null= True)
    create_at = models.DateField(null= True, default=None)
    id_product = models.ForeignKey(Book, models.CASCADE, db_column='ID_product', blank=True, null=True)
    num = models.IntegerField(null= True) 
    is_sale = models.BooleanField(default= True, null= True)
