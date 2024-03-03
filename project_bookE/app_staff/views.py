import email
from re import S
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib import messages, auth
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from app_order.models import *
from app_user.views import *
from django.core.paginator import Paginator
from django.db.models import Q
from app_store.forms import *
import datetime
from datetime import date
import time
import jwt
from .forms import * 
# Create your views here.

class isStaff(object):
    def dispatch(self, request, *args, **kwargs):
        if 'staff' in list(request.session.keys()):
            if request.session['staff']  is not None and Staff.objects.filter(email = request.session['staff'][1] , is_active = True, is_staff = True).exists() :
                pass
            else:
                messages.error(request=self.request, message="Bạn không có quyền truy cập")
                return redirect("adminlogin")
        else:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)
class isAdmin(object):
    def dispatch(self, request, *args, **kwargs):
        if 'staff' in list(request.session.keys()):
            if request.session['staff']  is not None and Staff.objects.filter(email = request.session['staff'][1] , is_active = True, is_staff = True, is_admin= True).exists() :
                pass
            else:
                messages.error(request=self.request, message="Bạn không có quyền truy cập")
                return redirect("adminlogin")
        else:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)
class LoginStaffView(View):
    
    template_name = "admin/adminlogin.html"
    def get(self, request, *args, **kwargs):
        # Staff.objects.create_superuser(id = 10, email= 'admin1@gmail.com',password = 'pbkdf2_sha256$390000$EOtgMhNhY3IOJVm0vXjW3F$vrEZilVU0IteqPr6fVO2e5pu/kKjhNa4HxVh6pt6DTo=', fullname='abc', username = 'abc')
        # if  request.session['staff'] is not None:
        request.session['staff'] = None
        return render(request, self.template_name)
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)
        user= None
        if len(Account.objects.using('admin').filter(email= email, is_active = True))>0:
            user = Account.objects.using('admin').get(email= email)
            if check_password(password, user.password) == True:
                user = user
            else:
                user = None
        else:
            user= None
        # user = authenticate( email=email, password=password, using='admin')
       
      
        # user = auth.authenticate(email=email, password=password)
        print(email, password)
        print(user)
        print('--------------------------------------')

        if user is not None:
            # auth.login(request=request, user=user,  using='admin')
            messages.success(request=request, message="Đăng nhập thành công!")
            # if user.is_admin == False:
            #     return redirect('home')
            # else:
            #     # return redirect('adminhome')
            #     pass
            user_list = [user.id,user.email,user.username,user.is_admin]
            
            request.session['staff'] = user_list
            return redirect('adminhome')
        else:
            messages.error(request=request, message="Đăng nhập thất bại")

        context = {
        'email': email if 'email' in locals() else '',
        'password': password if 'password' in locals() else '',
        }

        return render(request, 'admin/adminlogin.html', context=context) 

class AdminCreateStaffView(View,isAdmin):
    template_name = "admin/admincreatestaff.html"


    def get(self, request, *args, **kwargs):
        form = StaffForm
        staff = self.request.session['staff']
        context = {"form":form, 'staff':staff}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = StaffForm(data=request.POST)
        if form.is_valid():
            try:
                fullname = form.cleaned_data['fullname']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']
                username = email.split('@')[0]
                all_staff = Staff.objects.all()
                max_id = 0
                position = form.cleaned_data['position']
                salary = form.cleaned_data['salary']
                note = form.cleaned_data['note']
                today = date.today()
                for staff in all_staff:
                    max_id = max(max_id,staff.id)
                user = Staff.objects.create_user(id = max_id+1,
                    fullname=fullname, email=email, username=username, password=password)
                user.position= position
                user.salary= salary
                user.note= note
                user.date_created= today
                user.start_date= today
                user.phone_number = phone_number
                user.is_active = True
                user.is_staff = True
                user.save()
              
            
                messages.success(request=request, message="Thêm nhân viên thành công")
                return redirect('adminstafflist')
            except:
                messages.error(request=request, message="Thêm nhân viên thất bại")
        else:
            messages.error(request=request, message="Thêm nhân viên thất bại")
        staff = self.request.session['staff']
        
        context = {
                'form': form,
                'staff':staff

            }
        return render(request, 'admin/admincreatestaff.html', context)

class AdminStaffListView(isAdmin,isStaff, TemplateView):
    template_name = "admin/adminstafflist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        if kw is not None:
            queryset = Staff.objects.filter(
                Q(id__icontains=kw) |Q(fullname__icontains=kw)| Q(username__icontains=kw), is_staff= True, is_admin= False)
            paginator = Paginator(queryset, 20)
            page_number = self.request.GET.get('page')
            queryset = paginator.get_page(page_number)
        else:
            queryset = Staff.objects.filter(is_admin = False).order_by("-id")
            paginator = Paginator(queryset, 20)
            page_number = self.request.GET.get('page')
            queryset = paginator.get_page(page_number)
        staff = self.request.session['staff']
        context['staff']=  staff
        context["allstaffs"] = queryset
    
        return context

class AdminStaffDisableView(isAdmin,isStaff, View):
    template_name = "admin/adminuserlist.html"
    
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs["user_id"]
        account = Staff.objects.get(id = user_id)
        account.is_active = False
        account.save()
        queryset = Staff.objects.filter(is_admin = False).order_by("-id")
        paginator = Paginator(queryset, 20)
        page_number = self.request.GET.get('page')
        queryset = paginator.get_page(page_number)
        messages.success(request=request, message="Tắt hoạt động thành công")
        return redirect(reverse_lazy("adminstafflist"))

class AdminStaffEnableView(isAdmin,isStaff, View):
    template_name = "admin/adminstafflist.html"
    
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs["user_id"]
        account = Staff.objects.get(id = user_id)
        account.is_active = True
        account.save()
        queryset = Staff.objects.filter(is_admin= False).order_by("-id")
        paginator = Paginator(queryset, 20)
        page_number = self.request.GET.get('page')
        queryset = paginator.get_page(page_number)
        messages.success(request=request, message="Bật hoạt động thành công")
        return redirect(reverse_lazy("adminstafflist"))

class AdminEditStaffView( isAdmin,isStaff,View):
    template_name = "admin/admineditstaff.html"
    def get(self, request, *args, **kwargs):
        form = EditStaffForm()
        usr_id = kwargs['usr_id']
        user = Staff.objects.get(id = usr_id)
        form.fields['username'].initial  = user.username
        form.fields['phone_number'].initial  = user.phone_number
        form.fields['email'].initial  = user.email
        form.fields['fullname'].initial  = user.fullname
        form.fields['gender'].initial  = user.gender
        form.fields['dob'].initial = user.dob
        form.fields['position'].initial = user.position
        form.fields['salary'].initial = user.salary
        form.fields['note'].initial = user.note
        context = {'form': form, 'account': user  }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = EditStaffForm(data=request.POST)
        user= None
        if form.is_valid():
            try:
                usr_id = kwargs['usr_id']
                user = Staff.objects.get(id = usr_id)
                email = form.cleaned_data.get("email")
                username = form.cleaned_data.get("username")
                phone_number = form.cleaned_data.get("phone_number")
                fullname = form.cleaned_data.get("fullname")
                gender =  form.cleaned_data.get("gender")
                dob =  form.cleaned_data.get("dob")
                position =   form.cleaned_data.get("position")
                salary =   form.cleaned_data.get("salary")
                note =   form.cleaned_data.get("note")
                user.email = email
                user.username= username
                user.position = position
                user.salary = salary
                user.note = note
                user.dob = dob
                user.phone_number = phone_number
                user.fullname = fullname
                user.gender = gender
                user.save()
                messages.success(request=request, message="Cập nhật thành công")
            except:
                 messages.error(request=request, message="Cập nhật thất bại")
        else: 
            messages.error(request=request, message="Cập nhật thất bại")

        context = {
                'form': form, 'account': user
            }
        return render(request, self.template_name, context)

class AdminEditPersonalStaffView( isStaff,View):
    template_name = "admin/admineditpersonalstaff.html"
    def get(self, request, *args, **kwargs):
        form = EditPersonalStaffForm()
        usr_id = kwargs['usr_id']
        user = Staff.objects.get(id = usr_id)
        form.fields['username'].initial  = user.username
        form.fields['phone_number'].initial  = user.phone_number
        form.fields['email'].initial  = user.email
        form.fields['fullname'].initial  = user.fullname
        form.fields['gender'].initial  = user.gender
        form.fields['dob'].initial = user.dob
        form.fields['position'].initial = user.position
        form.fields['salary'].initial = user.salary
        form.fields['note'].initial = user.note
        context = {'form': form, 'account': user  }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = EditPersonalStaffForm(data=request.POST)
        user =None
        if form.is_valid():
            try:
                usr_id = kwargs['usr_id']
                user = Staff.objects.get(id = usr_id)
                phone_number = form.cleaned_data.get("phone_number")
                fullname = form.cleaned_data.get("fullname")
                gender =  form.cleaned_data.get("gender")
                dob =  form.cleaned_data.get("dob")
                # position =   form.cleaned_data.get("position")
                # salary =   form.cleaned_data.get("salary")
                # note =   form.cleaned_data.get("note")
                # user.position = position
                # user.salary = salary
                # user.note = note
                user.dob = dob
                user.phone_number = phone_number
                user.fullname = fullname
                user.gender = gender
                user.save()
                messages.success(request=request, message="Cập nhật thành công")
            except:
                
                 messages.error(request=request, message="Cập nhật thất bại")
        else: 
            messages.error(request=request, message="Cập nhật thất bại")

        context = {
                'form': form, 'account': user
            }
        return render(request, self.template_name, context)
class AdminHomeView( isStaff,TemplateView):
    template_name = "admin/adminhome.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = self.request.session['staff']
        context['staff']=  staff
        return context





   

class AdminPendingOrder(isStaff, TemplateView):
    template_name = "admin/adminpendingorders.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            status="Chờ xác nhận").order_by("-id")
        staff = self.request.session['staff']
        context['staff']=  staff
        return context

ORDER_STATUS = (
    ("Chờ xác nhận", "Chờ xác nhận"),
    ("Đã xác nhận", "Đã xác nhận"),
    ("Đang giao hàng", "Đang giao hàng"),
    ("Hoàn thành", "Hoàn thành"),
    ("Đơn hàng đã bị huỷ", "Đơn hàng đã bị huỷ"),
)


class AdminOrderDetailView(isStaff,DetailView,LoginRequiredMixin):
    template_name = "admin/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        staff = self.request.session['staff']
        context['staff']=  staff
        return context

class AdminOrderStatusChangeView(isStaff, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        try:
            order_obj = Order.objects.get(id=order_id)
            new_status = request.POST.get("status")
            order_obj.status = new_status
            order_obj.save()
            if len(list(set(list(OrderHistoryLog.objects.all().values_list('id', flat=True)))))>0:
                max_id = max(list(set(list(OrderHistoryLog.objects.all().values_list('id', flat=True)))))
            else:
                max_id = 0
            staff =  Staff.objects.get(id = request.session['staff'][0] )
            orderlog = OrderHistoryLog.objects.create(id= max_id+1,id_order = order_obj.id, status_current = order_obj.status,action_by_type_user ='staff',id_user = request.session['staff'][0],date_modifided= datetime.datetime.now(),id_staff = staff)
            messages.success(request=request, message="Thay đổi thành công")
        except:
            messages.error(request=request, message="Thay đổi thất bại")

        return redirect(reverse_lazy("adminorderdetail", kwargs={"pk": order_id}))
        
# Xem danh sách đơn hàng
class AdminOrderListView(isStaff,TemplateView):
    template_name = "admin/adminorderlist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        if kw is not None:
            queryset = Order.objects.filter(
                Q(id__icontains=kw))
            paginator = Paginator(queryset, 20)
            page_number = self.request.GET.get('page')
            queryset = paginator.get_page(page_number)
           
        else:
            queryset = Order.objects.all().order_by("-id")
            paginator = Paginator(queryset, 20)
            page_number = self.request.GET.get('page')
            queryset = paginator.get_page(page_number)
        context["allorders"] = queryset
        staff = self.request.session['staff']
        context['staff']=  staff
        return context

class AdminImportListView(isStaff, TemplateView):
    template_name = "admin/adminimportlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
      
        kw = self.request.GET.get("keyword")
        if kw is not None:
            queryset = ImportBook.objects.filter(
                Q(id__icontains=kw) | Q(id_product__name__icontains=kw) | Q(id_product__author__icontains=kw))
            paginator = Paginator(queryset, 10)
            page_number = self.request.GET.get('page')
            queryset = paginator.get_page(page_number)
        else:
            queryset = ImportBook.objects.all().order_by("-id")
            paginator = Paginator(queryset, 10)
            page_number = self.request.GET.get('page')
            queryset = paginator.get_page(page_number)
        context["allimport"] = queryset
        # context["allcategory"] =  allcategory
        staff = self.request.session['staff']
        context['staff']=  staff
        return context

class AdminImportView(isStaff, TemplateView):

    def get(self, request, *args, **kwargs):
        form = ImportForm()
        url_slug = kwargs['slug']
        product =  Book.objects.get(slug=url_slug)
        staff = self.request.session['staff']
        context = {'form': form,"product":product,'staff':staff}
        return render(request, "admin/adminimport.html", context)
    
    def post(self, request, *args, **kwargs):
        form = ImportForm(data=request.POST)
        if form.is_valid():
            price_import = form.cleaned_data['price_import']
            price_sale = form.cleaned_data['price_sale']
            num = form.cleaned_data['num']
            url_slug = kwargs['slug']
            product = Book.objects.get(slug=url_slug)
            id  = max(list(set(list(ImportBook.objects.all().values_list('id', flat=True))))) +1
            today = date.today()
            importbook = ImportBook.objects.create(id = id, price_import = price_import,price_sale = price_sale, create_at = today, id_product = product, num = num)
            if   product.stock is None:
                a = 0
            else :
                a =   product.stock
            product.stock =  a +num
            product.price =  price_sale
            product.save()

            list_import = ImportBook.objects.filter(id_product =  product)

            if list_import is not None:
                for i in list_import:
                    if i.id !=id :
                        i.is_sale = False 
                        i.save()
            staff = self.request.session['staff']
       

            context = {'form': form, "product": product,"staff":staff}
        return render(request, "admin/adminimport.html", context)

class AdminProductListView(isStaff, TemplateView):
    template_name = "admin/adminproductlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        allcategory = Category.objects.all().order_by("-id")
        
        kw = self.request.GET.get("keyword")
        if kw is not None:
            queryset = Book.objects.filter(
                Q(id__icontains=kw) | Q(name__icontains=kw) | Q(author__icontains=kw))
            paginator = Paginator(queryset, 10)
            page_number = self.request.GET.get('page')
            queryset = paginator.get_page(page_number)
        else:
            queryset = Book.objects.all().order_by("-id")
            paginator = Paginator(queryset, 10)
            page_number = self.request.GET.get('page')
            queryset = paginator.get_page(page_number)
        context["allproducts"] = queryset
        context["allcategory"] =  allcategory
        staff = self.request.session['staff']
        context['staff']=  staff
        return context

class AdminProductCreateView(isStaff, View):
    template_name = "admin/adminproductcreate.html"

    def get(self, request, *args, **kwargs):
        cagetoryid = kwargs["cate_id"]
        category = Category.objects.get(id = cagetoryid)
        form = BookForm()
        staff = self.request.session['staff']
     
        context = {'form': form,'category':category, "staff":staff}
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        cagetoryid = kwargs["cate_id"]
        form = BookForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            price = form.cleaned_data.get("price")
            short_description = form.cleaned_data.get("short_description")
            author = form.cleaned_data.get("author")
            slug   = form.cleaned_data.get("slug")
            is_authenic   = form.cleaned_data.get("is_authenic")
            publisher   = form.cleaned_data.get("publisher")
            publication_year    = form.cleaned_data.get("publication_year")
            dimensions    = form.cleaned_data.get("dimensions")
            book_cover   = form.cleaned_data.get("book_cover")
            numpage    = form.cleaned_data.get("numpage")
            manufacturer    = form.cleaned_data.get("manufacturer")
            images = self.request.FILES.getlist("images")[0]
            max_id = max(list(set(list(Book.objects.all().values_list('id', flat=True)))))
            category = Category.objects.get(id = cagetoryid)
            p = Book.objects.create(id_category = category ,id = max_id+1,name = name, price= price, short_description = short_description, author= author,slug  = slug ,is_authenic= is_authenic, publisher= publisher, publication_year= publication_year, dimensions= dimensions, book_cover= book_cover , numpage= numpage,manufacturer= manufacturer,image = images)
            messages.success(request=request, message="Thêm sách thành công")
        else:
            messages.error(request=request, message="Thêm sách thất bại")
        return redirect(reverse_lazy("adminproductlist"))
class AdminProductDeleteView(isStaff, View):
    template_name = "admin/adminproductlist.html"
    
    def get(self, request, *args, **kwargs):
        allcategory = Category.objects.all().order_by("-id")
        pro_id = self.kwargs["pro_id"]
        product = Book.objects.get(id = pro_id)
        product.delete()
        queryset = Book.objects.all().order_by("-id")
        paginator = Paginator(queryset, 10)
        page_number = self.request.GET.get('page')
        queryset = paginator.get_page(page_number)
        messages.success(request=request, message="Xóa sách thành công")
        return redirect(reverse_lazy("adminproductlist"))

class AdminProductDetailView(View):
    template_name = "admin/adminproductdetail.html"

    def get(self, request, *args, **kwargs):
        form = BookForm()
        pro_id = kwargs['pro_id']
        product = Book.objects.get(id=pro_id)
        form.fields['name'].initial = product.name 
        form.fields['price'].initial = product.price 
        form.fields['short_description'].initial = product.short_description 
        form.fields['author'].initial = product.author
        form.fields['slug'].initial = product.slug
        form.fields['is_authenic'].initial = product.is_authenic
        form.fields['publisher'].initial = product.publisher
        form.fields['publication_year'].initial = product.publication_year
        form.fields['dimensions'].initial = product.dimensions
        form.fields['book_cover'].initial = product.book_cover
        form.fields['numpage'].initial = product.numpage
        form.fields['manufacturer'].initial = product.manufacturer
        # form.fields['images'].initial =  product.image
        staff = self.request.session['staff']
      
        context = {'form': form, "product": product,'staff':staff}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = BookForm(data=request.POST)
        pro_id = kwargs['pro_id']
        product = Book.objects.get(id=pro_id)
        if form.is_valid():
            name  = form.cleaned_data.get("name")
            price = form.cleaned_data.get("price")
            short_description = form.cleaned_data.get("short_description")
            slug = form.cleaned_data.get("slug")
            author = form.cleaned_data.get("author")
            is_authenic = form.cleaned_data.get("is_authenic")
            publisher = form.cleaned_data.get("publisher")
            publication_year = form.cleaned_data.get("publication_year")
            dimensions = form.cleaned_data.get("dimensions")
            book_cover = form.cleaned_data.get("book_cover")
            numpage = form.cleaned_data.get("numpage")
            manufacturer = form.cleaned_data.get("manufacturer")
            if len( self.request.FILES.getlist("images"))>0: 
                images = self.request.FILES.getlist("images")[0]
                product.image = images
            product.name = name
            product.price = price
            product.short_description  =  short_description
            product.slug = slug
            product.author= author
            product.is_authenic= is_authenic
            product.publisher= publisher
            product.publisher_year = publication_year
            product.dimensions= dimensions
            product.book_cover= book_cover
            product.numpage= numpage
            product.manufacturer = manufacturer
            product.is_upload = True
            product.save()
            messages.success(request=request, message="Sửa sách thành công")
        else:
            messages.error(request=request, message="Xóa sách thất bại")
        staff = self.request.session['staff']
       
        context = {'form': form, "product": product,'staff':staff}
        
          
        return render(request, self.template_name, context)


class AdminUserDisableView(isStaff, View):
    template_name = "admin/adminuserlist.html"
    
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs["user_id"]
        account = Customer.objects.get(id = user_id)
        account.is_active = False
        account.save()
        queryset = Customer.objects.all().order_by("-id")
        paginator = Paginator(queryset, 20)
        page_number = self.request.GET.get('page')
        queryset = paginator.get_page(page_number)
        messages.success(request=request, message="Tắt hoạt động thành công")
        return redirect(reverse_lazy("adminuserlist"))

class AdminUserEnableView(isStaff, View):
    template_name = "admin/adminuserlist.html"
    
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs["user_id"]
        account = Customer.objects.get(id = user_id)
        account.is_active = True
        account.save()
        queryset = Customer.objects.all().order_by("-id")
        paginator = Paginator(queryset, 20)
        page_number = self.request.GET.get('page')
        queryset = paginator.get_page(page_number)
        messages.success(request=request, message="Bật hoạt động thành công")
        return redirect(reverse_lazy("adminuserlist"))

class AdminUserListView(isStaff, TemplateView):
    template_name = "admin/adminuserlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        if kw is not None:
            queryset = Customer.objects.filter(
                Q(id__icontains=kw) |Q(fullname__icontains=kw)| Q(username__icontains=kw))
            paginator = Paginator(queryset, 20)
            page_number = self.request.GET.get('page')
            queryset = paginator.get_page(page_number)
        else:
            queryset = Customer.objects.all().order_by("-id")
            paginator = Paginator(queryset, 20)
            page_number = self.request.GET.get('page')
            queryset = paginator.get_page(page_number)
        staff = self.request.session['staff']
        context['staff']=  staff
        context["allusers"] = queryset
    
        return context

# class AdminDashboardView(isStaff, TemplateView):
#     # template_name = "adminpages/dashboard.html"
#     def signed_public_dashboard(request):
#         # METABASE_SITE_URL = "http://localhost:3000"
#         METABASE_SITE_URL = " https://b614-2405-4803-fba7-2d70-98af-c23-91b4-f514.ngrok-free.app"
#         METABASE_SECRET_KEY = "31d52c0025a66928fe84508c126bf1883d097239b0ce81f3c126ec02c764a51a"

#         payload = {
#         "resource": {"dashboard": 97},
#         "params": {
            
#         },
#         "exp": round(time.time()) + (60 * 10) # 10 minute expiration
#         }
#         token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

#         iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true&refresh=1"
      
#         staff = request.session['staff']
      
#         return render(request,
#                     "admin/dashboard.html",
#                     {'iframeUrl': iframeUrl,'staff':staff}) 
                    