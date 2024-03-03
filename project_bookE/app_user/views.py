from re import split
from unittest.mock import NonCallableMagicMock

from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from .forms import RegisterForm, EditProfileForm,  AddressShippingForm
from .models import Customer, AddressShipping
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
import requests
import datetime



class RegisterView(View):
    template_name = "app_user/register.html"

    def get(self, request, *args, **kwargs):
        form = RegisterForm
        context = {"form":form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            all_account = Customer.objects.all()
            max_id = 0
            for account in all_account:
                max_id = max(max_id,account.id)
            user = Customer.objects.create_user(id = max_id+1,
                fullname=fullname, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.is_active = True
            user.date_created  = datetime.datetime.now()
            user.save()
            print(fullname)
            print(user.fullname)

            # current_site = get_current_site(request=self.request)
            # mail_subject = 'Activate your blog account.'
            # message = render_to_string('accounts/active_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user)
            # })
            # send_email = EmailMessage(mail_subject, message, to=[email])
            # send_email.send()

            # messages.success(
            #     request= request,
            #     message="Please check your email to activate your account."
            # )
            messages.success(request=request, message="Đăng kí thành công")
            return redirect('register')
        else:
            messages.error(request=request, message="Đăng kí thất bại")
        context = {
                'form': form,
            }
        return render(request, 'app_user/register.html', context)



class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(id = request.user.id, is_active = True).exists() :
            pass
           
        else:
            messages.warning(request=request, message="Bạn cần phải đăng nhập")
            return render(request, 'app_user/login.html')
        return super().dispatch(request, *args, **kwargs)



class isCustomer(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(id = request.user.id, is_active = True, is_staff = False).exists() :
            pass
        else:
            return redirect("login")
           
        return super().dispatch(request, *args, **kwargs)
class LoginView(View):
    template_name = "app_user/login.html"
    def get(self, request, *args, **kwargs):
        if request.user is not None:
              logout(request)
        return render(request, self.template_name)
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        print(email, password)
        print(user)

        if user is not None:
            auth.login(request=request, user=user)
            messages.success(request=request, message="Đăng nhập thành công")
            # if user.is_admin == False:
            #     return redirect('home')
            # else:
            #     # return redirect('adminhome')
            #     pass
            return redirect('home')
        else:
            messages.error(request=request, message="Đăng nhập thất bại")

        context = {
        'email': email if 'email' in locals() else '',
        'password': password if 'password' in locals() else '',
        }

        return render(request, 'app_user/login.html', context=context) 


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request=request, message="Đăng xuất thành công")
        return redirect("home")

class ProfileView(TemplateView, LoginRequiredMixin,isCustomer):
    template_name = "app_user/profile.html"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(id = request.user.id, is_admin = False, is_superadmin= False  ).exists():
            pass
        elif request.user.is_authenticated and Customer.objects.filter(id = request.user.id, is_admin = True, is_superadmin= True  ).exists():
            return redirect('adminhome')
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # kw = self.request.GET.get("keyword")
        account = Customer.objects.get(id = self.request.user.id)
        context['account'] = account
        # if kw is not None:
        #     orders = Order.objects.filter (Q(id__icontains=kw))
        # else:
        #     orders = Order.objects.filter(customerid=customer).order_by("-id")
        # context["orders"] = orders
        return context

class EditProfileView( LoginRequiredMixin,View):
    template_name = "app_user/profile_edit.html"
    def get(self, request, *args, **kwargs):
        form = EditProfileForm()
        usr_id = kwargs['usr_id']
        user = Customer.objects.get(id = usr_id)
        form.fields['username'].initial  = user.username
        form.fields['phone_number'].initial  = user.phone_number
        form.fields['email'].initial  = user.email
        form.fields['fullname'].initial  = user.fullname
        form.fields['gender'].initial  = user.gender
        form.fields['dob'].initial = user.dob

        context = {'form': form, 'account': user }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = EditProfileForm(data=request.POST)
        if form.is_valid():
            usr_id = kwargs['usr_id']
            user = Customer.objects.get(id = usr_id)
            phone_number = form.cleaned_data.get("phone_number")
            fullname = form.cleaned_data.get("fullname")
            gender =  form.cleaned_data.get("gender")
            dob =  form.cleaned_data.get("dob")

            user.dob = dob
            user.phone_number = phone_number
            user.fullname = fullname
            user.gender = gender
            user.save()
            messages.success(request=request, message="Cập nhật thành công")
        else: 
            messages.error(request=request, message="Cập nhật thất bại")

        context = {
                'form': form, 'account': user
            }
        return redirect("profile")


class ShippingAddressCreateView(LoginRequiredMixin, View):
    template_name = "app_user/shippingaddresscreate.html"

    def get(self, request, *args, **kwargs):
        form = AddressShippingForm()
        cus_id = kwargs['cus_id']
        account = Customer.objects.get(id = cus_id)
        context = {"form":form, 'account': account}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form =  AddressShippingForm(request.POST)
        if form.is_valid():
            cus_id = kwargs['cus_id']
            account = Customer.objects.get(id = cus_id)
            name_receiver = form.cleaned_data.get("name_receiver")
            receiver_phone = form.cleaned_data.get("receiver_phone")
            city = form.cleaned_data.get("city")
            district = form.cleaned_data.get("district")
            ward = form.cleaned_data.get('ward')
            address_detail = form.cleaned_data.get('address_detail')
            if len(list(set(list(AddressShipping.objects.all().values_list('id', flat=True)))))>0:
                max_id = max(list(set(list(AddressShipping.objects.all().values_list('id', flat=True)))))
            else:
                max_id=0
            addressshipping = AddressShipping.objects.create(id = max_id+1,city = city, district = district, ward = ward, address_detail = address_detail, name_receiver = name_receiver, receiver_phone = receiver_phone, account = account)
            
            shippingaddresslist = AddressShipping.objects.filter(account = account)
            context = {"form":form, "shippingaddresslist":shippingaddresslist, "account" : account}
            messages.success(request=request, message="Tạo địa chỉ thành công")
        else: 
            messages.error(request=request, message="Tạo địa chỉ thất bại")
       
        return render(request, "app_user/shippingaddresslist.html", context)

class ShippingAddressListView(LoginRequiredMixin,View):
    template_name = "app_user/shippingaddresslist.html"
    def get(self, request, *args, **kwargs):
        cus_id = kwargs['cus_id']
        account = Customer.objects.get(id = cus_id)
        shippingaddresslist = AddressShipping.objects.filter(account = account, is_active = True)
        if len(shippingaddresslist) == 0: 
            shippingaddresslist = None
        context = {"shippingaddresslist" : shippingaddresslist, "account" : account}
        return render(request, self.template_name, context)

class ShippingAddressEditView(LoginRequiredMixin, View):
    template_name = "app_user/shippingaddressedit.html"

    def get(self, request, *args, **kwargs):
        cus_id = kwargs['cus_id']
        account = Customer.objects.get(id = cus_id)
        form = AddressShippingForm()
        addr_id = kwargs['addr_id']
        shippingaddress = AddressShipping.objects.get(id = addr_id)
        form.fields['name_receiver'].initial  = shippingaddress.name_receiver
        form.fields['city'].initial  = shippingaddress.city
        form.fields['district'].initial  =shippingaddress.district
        form.fields['ward'].initial  = shippingaddress.ward
        form.fields['address_detail'].initial  = shippingaddress.address_detail
        form.fields['receiver_phone'].initial  = shippingaddress.receiver_phone
        context = {"form":form,'account':account}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AddressShippingForm(request.POST)
        if form.is_valid():
            cus_id = kwargs['cus_id']
            addr_id = kwargs['addr_id']
            account = Customer.objects.get(id = cus_id)
            city = form.cleaned_data.get("city")
            district = form.cleaned_data.get("district")
            ward = form.cleaned_data.get("ward")
            address_detail = form.cleaned_data.get("address_detail")
            name_receiver = form.cleaned_data.get("name_receiver")
            receiver_phone = form.cleaned_data.get("receiver_phone")
            addressshipping = AddressShipping.objects.get(id = addr_id)
            addressshipping.city = city
            addressshipping.district = district
            addressshipping.ward = ward
            addressshipping.address_detail = address_detail
            addressshipping.name_receiver = name_receiver
            addressshipping.receiver_phone = receiver_phone
            addressshipping.save()
            shippingaddresslist = AddressShipping.objects.filter(account = account)
            context = {"form":form, "shippingaddresslist":shippingaddresslist, "account" : account}
            messages.success(request=request, message="Cập nhật địa chỉ thành công")
        else:
            messages.error(request=request, message="Cập nhật địa chỉ thất bại")

        return render(request, "app_user/shippingaddresslist.html", context)

class ShippingAddressDeleteView(LoginRequiredMixin,View):
    template_name = "app_user/shippingaddresslist.html"
    def get(self, request, *args, **kwargs):
        addr_id = kwargs['addr_id']
        if addr_id is not None:
            if len(list(AddressShipping.objects.filter(id = addr_id))) >0:
                addressshipping = AddressShipping.objects.get(id = addr_id)
                addressshipping.is_active = False
                addressshipping.save()
        cus_id = kwargs['cus_id']
        account = Customer.objects.get(id = cus_id)
        shippingaddresslist = AddressShipping.objects.filter(account = account, is_active= True)
        context = {"shippingaddresslist":shippingaddresslist, "account" : account}
        messages.success(request=request, message="Xóa địa chỉ thành công")
        
        # return redirect("shippingaddresslist")
        return render(request, self.template_name, context)

