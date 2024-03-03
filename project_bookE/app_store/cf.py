import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from app_store.models import *
import pandas as pd
from django.conf import settings

# def recommendation(request): 
#     list_product_re = []
#     rated = True
#     if  request.user is not None :
#         user_id = request.user.id
#         if len(Customer.objects.filter(id =user_id))>0:
#             account =  Customer.objects.get(id =user_id)
#             user_rated = list(set(list(RatingBook.objects.all().values_list('id_customer', flat=True))))
#             if account.is_admin == False and account.is_admin == False and account.id in user_rated:
#                 book_rated = list(set(list(RatingBook.objects.all().values_list('id_product', flat=True))))
#                 books_user_rated = list(set(list(RatingBook.objects.filter(id_customer=user_id).values_list('id_product', flat=True))))
#                 max_user_rating = max(list(set(list(RatingBook.objects.all().values_list('id_customer', flat=True)))))
#                 product_id  = []
#                 for book_id in book_rated:
#                     if book_id  not in  books_user_rated:
#                         product_id.append(book_id)
#                 print(len(product_id))
#                 model_path = settings.MODEL_PATH
#                 model = load_model(model_path)
#                 book_data = np.array([i for i in product_id])
#                 user = np.array([user_id for i in range(len(product_id))])
#                 predictions = model.predict([user, book_data])
#                 predictions = np.array([a[0] for a in predictions])
#                 list_id_pr = (-predictions).argsort()[:6]
              
            
#                 for i in list_id_pr:
#                     product = Book.objects.get(id = i)
#                     list_product_re.append(product)
#             else:
#                 products =  Book.objects.filter(count_review__isnull=False).order_by('-count_review')
#                 list_product_re = products[:6]
#                 rated= False
                
#         else:
#             products =  Book.objects.filter(count_review__isnull=False).order_by('-count_review')
#             list_product_re = products[:6]
#             rated= False
#     else:
#         products =  Book.objects.filter(count_review__isnull=False).order_by('-count_review')
#         list_product_re = products[:6]
#         rated= False
#   return dict(product_recommend= list_product_re, rated = rated)

def get_book_id(user_id):
    #lấy các sách đã có đánh giá mà khách hàng chưa đánh giá
    book_rated = list(set(list(RatingBook.objects.all().values_list('id_product', flat=True))))
    books_user_rated = list(set(list(RatingBook.objects.filter(id_customer=user_id).values_list('id_product', flat=True))))
    max_user_rating = max(list(set(list(RatingBook.objects.all().values_list('id_customer', flat=True)))))
    product_id  = []
    for book_id in book_rated:
        if book_id  not in  books_user_rated:
            product_id.append(book_id)
    return product_id

def top6_avg_rating(category_id = None):
    list_product =  []
    if category_id is  None:
        products =  Book.objects.filter(avg_rating__isnull=False).order_by('-avg_rating')
        list_product = products[:6]
    else:
        products =  Book.objects.filter(id_category = category_id,avg_rating__isnull=False).order_by('-avg_rating')
        list_product = products[:6]
    return list_product

def recommendation(request): 
    list_product_re = []
    rated = True
    if  request.user.id is not None : # khách hàng đăng nhập
        # đề xuất top 6 sách khách hàng có thể quan tâm
        user_id = request.user.id
        customer =  Customer.objects.get(id = user_id)
        user_rated = list(set(list(RatingBook.objects.all().values_list('id_customer', flat=True))))
        if customer.id in user_rated: # khách hàng đã đánh giá trên hệ thống
            product_id =  get_book_id(user_id)
            model_path = settings.MODEL_PATH
            model = load_model(model_path)
            book_data = np.array([i for i in product_id])
            user = np.array([user_id for i in range(len(product_id))])
            predictions = model.predict([user, book_data])
            predictions = np.array([a[0] for a in predictions])
            list_id_pr = (-predictions).argsort()[:6]
            for i in list_id_pr:
                product = Book.objects.get(id = i)
                list_product_re.append(product)
        else: # khách hàng chưa đánh giá trên hệ thống
            #Lấy top 6 sách được đánh giá cao
            list_product_re = top6_avg_rating()
            rated= False          
    else: # khách hàng chưa đăng nhập
        # Lấy top 6 sách được đánh giá cao
        list_product_re = top6_avg_rating()
        rated= False
    return dict(product_recommend= list_product_re, rated = rated)

def recommendation_filter_category(request,product_book): 
    category_id = product_book.id_category
    list_product_re = []
    rated = True
    if  request.user.id is not None : # khách hàng đăng nhập
        # đề xuất top 6 sách khách hàng có thể quan tâm
        user_id = request.user.id
        customer =  Customer.objects.get(id = user_id)
        user_rated = list(set(list(RatingBook.objects.all().values_list('id_customer', flat=True))))
        if customer.id in user_rated: # khách hàng đã đánh giá trên hệ thống
            product_id =  get_book_id(user_id)
            model_path = settings.MODEL_PATH
            model = load_model(model_path)
            book_data = np.array([i for i in product_id])
            user = np.array([user_id for i in range(len(product_id))])
            predictions = model.predict([user, book_data])
            predictions = np.array([a[0] for a in predictions])
            list_id_pr = (-predictions).argsort()[:]
            for i in list_id_pr:
                if  i == product_book.id:
                        continue
                if len(Book.objects.filter(id = i,id_category =  category_id)) >0:
                    product = Book.objects.get(id = i,id_category =  category_id)
                    list_product_re.append(product)
            list_product_re = list_product_re[:6]
        else: # khách hàng chưa đánh giá trên hệ thống
            #Lấy top 6 sách được đánh giá cao
            list_product_re = top6_avg_rating(category_id =  category_id)
            rated= False          
    else: # khách hàng chưa đăng nhập
        # Lấy top 6 sách được đánh giá cao
        list_product_re = top6_avg_rating(category_id =  category_id)
        rated= False
   
            
                
    return list_product_re
# def recommendation_filter_category(request,product_book): 
#     category_id = product_book.id_category
#     list_product_re = []
#     rated = True
#     if  request.user is not None :
#         user_id = request.user.id
#         if len(Customer.objects.filter(id =user_id))>0:
#             account =  Customer.objects.get(id =user_id)
#             user_rated = list(set(list(RatingBook.objects.all().values_list('id_customer', flat=True))))
#             if account.is_admin == False and account.is_admin == False and account.id in user_rated:
#                 book_rated = list(set(list(RatingBook.objects.all().values_list('id_product', flat=True))))
#                 books_user_rated = list(set(list(RatingBook.objects.filter(id_customer=user_id).values_list('id_product', flat=True))))
#                 max_user_rating = max(list(set(list(RatingBook.objects.all().values_list('id_customer', flat=True)))))
#                 product_id  = []
#                 for book_id in book_rated:
#                     if book_id  not in  books_user_rated:
#                         product_id.append(book_id)
#                 print(len(product_id))
#                 model_path = settings.MODEL_PATH
#                 model = load_model(model_path)
#                 book_data = np.array([i for i in product_id])
#                 user = np.array([user_id for i in range(len(product_id))])
#                 predictions = model.predict([user, book_data])
#                 predictions = np.array([a[0] for a in predictions])
#                 list_id_pr = (-predictions).argsort()[:]
              
            
#                 for i in list_id_pr:
#                     if  i == product_book.id:
#                         continue
#                     if len(Book.objects.filter(id = i,id_category =  category_id)) >0:
#                         product = Book.objects.get(id = i,id_category =  category_id)
#                         list_product_re.append(product)
#                 list_product_re = list_product_re[:6]
#             else:
#                 products =  Book.objects.filter(count_review__isnull=False, id_category =  category_id).order_by('-count_review')
#                 list_product_re = products[:6]
#                 rated= False
                
#         else:
#             products =  Book.objects.filter(count_review__isnull=False, id_category =  category_id).order_by('-count_review')
#             list_product_re = products[:6]
#             rated= False
#     else:
#         products =  Book.objects.filter(count_review__isnull=False, id_category =  category_id).order_by('-count_review')
#         list_product_re = products[:6]
#         rated= False
          
   
            
                
#     return list_product_re
    