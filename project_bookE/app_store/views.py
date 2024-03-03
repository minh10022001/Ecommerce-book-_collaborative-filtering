from ast import Import
from concurrent.futures import process
from this import d
from unicodedata import name
from django.shortcuts import render,get_object_or_404, redirect
from .models import *
from app_user.views import *
from django.core.paginator import Paginator
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
# from .cf import recommendation
from django.db.models import Q
from .forms import *
from datetime import date
from app_order.models import *
import datetime
import time
import jwt
from app_store.cf import recommendation_filter_category

# Create your views here.

# def home(request):
#     # products = Product.objects.all().filter(is_available=True)
#     # context = {
#     #     'products': products,
#     # }
#     return render(request, 'home.html')

def get_all_category(request):
    links = Category.objects.all()
    return dict(category=links)

def count_wish(request):
    count = 0
    if request.user is not None:
        print(request.user)
        user = request.user
        if Wishlistline.objects.filter(id_customer = user.id)   is None or len(Wishlistline.objects.filter(id_customer = user.id))==0:
            count= 0
        else:
            count = len(Wishlistline.objects.filter(id_customer = user.id))
    
    return dict(count_wish= count)
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        if 'staff' in list(self.request.session.keys()):
            self.request.session['staff'] = None
        else:
            pass
        if kw is not None:
            all_products = Book.objects.filter(Q(id__icontains=kw) | Q(name__icontains=kw) | Q(author__icontains=kw))
            paginator = Paginator(all_products, 18)
            page_number = self.request.GET.get('page')
            product_list = paginator.get_page(page_number)
        else:
            all_products = Book.objects.all()
            paginator = Paginator(all_products, 18)
            page_number = self.request.GET.get('page')
            product_list = paginator.get_page(page_number)
        if len(product_list) ==0:
            product_list = None
        context['product_list'] = product_list
        context['search'] =   kw
        if self.request.user.is_authenticated and Customer.objects.filter(id =  self.request.user.id).exists():
            customer = Customer.objects.get( id= self.request.user.id)
            if Wishlistline.objects.filter(id_customer = customer.id).exists():
                wishlistline = Wishlistline.objects.filter(id_customer = customer.id)
                context['wishListItem'] = wishlistline
            else:
                context['wishListItem'] = []

        # for i in all_products:
        #     all_feedback =  RatingBook.objects.filter(id_product = i.id)
        #     if all_feedback ==None or len(all_feedback)<1:
        #         i.count_review = 0
        #         i.avg_rating = 0
        #     else: 
        #         sum_rating = 0
        #         i.count_review = len(all_feedback)
        #         for j in all_feedback:
        #             sum_rating += j.rating
        #         i.avg_rating = round(sum_rating/len(all_feedback),1)
        #     i.save()
  

        all_account =  Account.objects.using("admin")
        print(all_account)
        all_category =  Category.objects.all()
        context['category'] = all_category

       
       
        return context

class UpdateToWishList(TemplateView,LoginRequiredMixin):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        action = self.request.GET.get("action")
        pro_id = self.kwargs["pro_id"]
        if kw is not None:
            all_products = Book.objects.filter(Q(id__icontains=kw) | Q(name__icontains=kw) | Q(author__icontains=kw))
            paginator = Paginator(all_products, 18)
            page_number = self.request.GET.get('page')
            product_list = paginator.get_page(page_number)
        else:
            all_products = Book.objects.all()
            paginator = Paginator(all_products, 18)
            page_number = self.request.GET.get('page')
            product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        context['search'] =   kw
        if self.request.user.is_authenticated and Customer.objects.filter(id =  self.request.user.id).exists():
            customer = Customer.objects.get( id= self.request.user.id)
            product = Book.objects.get(id = pro_id)
            if action =='add':
                try:
                    wishlistline = Wishlistline.objects.create(id_product = product, id_customer = customer, create_at =datetime.datetime.now() )
                    messages.success(request=self.request, message="Thêm vào danh sách yêu thích thành công")
                except:
                    messages.error(request=self.request, message="Thêm vào danh sách yêu thích thât bại")

            else:
                wishlistline = Wishlistline.objects.filter(id_product = product.id, id_customer = customer.id)
                for i in wishlistline:
                    i.delete()
                    messages.success(request=self.request, message="Xóa sản phẩm yêu thích thành công")
                
            if Wishlistline.objects.filter(id_customer = customer).exists():
                wishlistline = [i.id_product for i  in Wishlistline.objects.filter(id_customer = customer)]
                context['wishListItem'] = wishlistline
            else:
                context['wishListItem'] = []
        else:
            messages.error(request=self.request, message="Bạn cần phải đăng nhập để yêu thích sản phẩm")

        all_category =  Category.objects.all()
        context['category'] = all_category
        return context

class WishListView(LoginRequiredMixin,TemplateView):
    template_name = "app_store/wishlist.html"
    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated and Customer.objects.filter(id = self.request.user.id).exists():
            context = super().get_context_data(**kwargs)
            customer = Customer.objects.get(id = self.request.user.id)
            wishListItem = Wishlistline.objects.filter(id_customer = customer.id)
            context['wishListItem'] = wishListItem
            return context
        else:
            return redirect("home")
class ProductCategoryView(TemplateView):
    template_name = "app_store/categoryproduct.html"
    def get_context_data(self,**kwargs):
        category_slugs = kwargs['category_slug'] 
        print( category_slugs)
        context = super().get_context_data(**kwargs)
        categories = get_object_or_404(Category, slug_category=category_slugs)
        all_products = Book.objects.all().filter(id_category=categories.id)
        paginator = Paginator(all_products, 18)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        context['category1'] = categories
        print(categories)

        return context

class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        form = RatingForm()
        url_slug = kwargs['slug']
        product =  Book.objects.get(slug=url_slug)
        context = {'form': form,"product":product}
        feedbacks = RatingBook.objects.filter(id_product = product.id).order_by('-create_at')
        context['feedbacks'] = feedbacks
        is_rated = False
        if request.user.id is None:
            is_rated = False
        else:
            if len(Order.objects.filter(customerid  = request.user))>0:
                orders  = Order.objects.filter(customerid  = request.user)
                for order in orders:
                    if len(Orderitem.objects.filter(orderid = order.id, product = product))>0 and order.status =='Hoàn thành':
                            is_rated = True
                            break
              
            else:
                is_rated = False
        if len(RatingBook.objects.filter(id_product= product, id_customer = request.user.id )) >0:
            is_rated =  False
        product_r = recommendation_filter_category(request, product)


        context['is_rated'] =  is_rated
        context['product_r'] = product_r
        print(str(is_rated) +'----------------------------------------------------')

        return render(request, 'app_store/productdetail.html', context)
    
    def post(self, request, *args, **kwargs):
        form = RatingForm(data=request.POST)
        url_slug = kwargs['slug']
        product = Book.objects.get(slug=url_slug)
        feedbacks = RatingBook.objects.filter(id_product= product)
        if form.is_valid():
            try:
                content = form.cleaned_data['content']
                rate = form.cleaned_data['rating']
                url_slug = kwargs['slug']
                product = Book.objects.get(slug=url_slug)
                customer = Customer.objects.get(id = request.user.id)
                id  = max(list(set(list(RatingBook.objects.all().values_list('id', flat=True))))) +1
                today = date.today()
                feedback = RatingBook.objects.create(id = id,id_product = product, id_customer = customer, content = content, rating = rate, create_at = today)
                feedback.save()
                messages.success(request=self.request, message="Đánh giá thành công")
                feedbacks = RatingBook.objects.filter(id_product= product)
            
                # if feedbacks ==None:
                #     product.count_review = 0
                #     product.avg_rating = 0
                #     product.save()
                # else: 
                #     sum_rating = 0
                #     product.count_review = len(feedbacks)
                #     for j in feedbacks:
                #         sum_rating += j.rating
                #     product.avg_rating = round(sum_rating/len(feedbacks),1)
                #     product.save()
            except:
                messages.error(request=self.request, message="Đánh giá thất bại")
                # context = {'form': RatingForm(), "product": product, "feedbacks": feedbacks}
            
        else:
            messages.error(request=self.request, message="Đánh giá thất bại")
        is_rated = True
        if request.user.id is None:
            is_rated = False
        else:
            if len(Order.objects.filter(customerid  = request.user))>0:
                orders  = Order.objects.filter(customerid  = request.user)
                for order in orders:
                    if len(Orderitem.objects.filter(orderid = order.id, product = product))>0 and order.status =='Hoàn thành':
                            is_rated = True
                            break
            else:
                is_rated = False
        if len(RatingBook.objects.filter(id_product= product, id_customer = request.user.id )) >0:
            is_rated =  False
        print(str(is_rated) +'----------------------------------------------------')
        product_r = recommendation_filter_category(request, product)
        context = {'form': RatingForm(), "product": product, "feedbacks": feedbacks,"product_r":product_r}
        return render(request, 'app_store/productdetail.html', context)

class MyRatingView(TemplateView, LoginRequiredMixin):
    template_name = "app_store/myrating.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cus_id = kwargs['cus_id']
        kw = self.request.GET.get("keyword")
        customer = Customer.objects.get(id = cus_id)
        context['customer'] = customer
        if kw is not None:
            ratings= RatingBook.objects.filter (Q(id__icontains=kw))
        else:
            ratings = RatingBook.objects.filter(id_customer=customer).order_by("-id")
        if len(ratings) == 0:
            ratings = None
        context["rating"] = ratings
        context['account'] =  customer
        return context








    
 
