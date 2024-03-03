from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from app_user.views import *



def  count_items_cart(request):
    count = 0
    if request.user is not None:
        print(request.user)
        user = request.user
        if Shoppingcart.objects.filter(customerid = user.id)   is None or len(Shoppingcart.objects.filter(customerid = user.id))==0:
            count= 0
        else:
            print(len(Shoppingcart.objects.filter(customerid = user.id )))
            cart = Shoppingcart.objects.filter(customerid = user.id)[0]
        
            if Cartline.objects.filter(shoppingcartid  =cart) is  None:
                count =0
            else:
                cartlinelist = Cartline.objects.filter(shoppingcartid  =cart, is_active = True)
                for cartline in cartlinelist:
                    count+=1
    
    return dict(count_cart= count)

class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = get_object_or_404(Shoppingcart, id=cart_id)
            if request.user.is_authenticated and request.user:
                cart_obj.customerid = Customer.objects.get(id = self.request.user.id)
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)

class AddToCartView( LoginRequiredMixin, EcomMixin, View):
        def get(self, request, *args, **kwargs):
            product_id = self.kwargs['pro_id']
        # get product
            product_obj = Book.objects.get(id=product_id)
            if self.request.user.is_authenticated and Customer.objects.filter(id = self.request.user.id).exists():
                customer = Customer.objects.get(id = self.request.user.id)
                # check if cart exists
                cart_id = self.request.session.get("cart_id", None)
                if cart_id:
                    cart_obj = Shoppingcart.objects.get(id=cart_id)
                    this_product_in_cart = Cartline.objects.filter(id_product = product_obj, is_active = True)

                    # item already exists in cart
                    if this_product_in_cart.exists():
                        cartproduct = this_product_in_cart.last()
                        cartproduct.num += 1
                        cartproduct.save()
                        cart_obj.save()
                    # new item is added in cart
                    else:
                        if len(list(set(list(Cartline.objects.all().values_list('id', flat=True)))))>0:
                            max_id = max(list(set(list(Cartline.objects.all().values_list('id', flat=True)))))
                        else:
                            max_id = 0
                        cartproduct = Cartline.objects.create(id= max_id+1,
                            shoppingcartid=cart_obj, id_product=product_obj, num=1)
                        cart_obj.save()

                else:
                    if Shoppingcart.objects.filter(customerid = customer).exists():
                        cart_obj = Shoppingcart.objects.get(customerid = customer)
                        this_product_in_cart = Cartline.objects.filter(id_product= product_obj, is_active = True)

                        # item already exists in cart
                        if this_product_in_cart.exists():
                            cartproduct = this_product_in_cart.last()
                            cartproduct.num += 1
                            cartproduct.save()
                            cart_obj.save()
                        # new item is added in cart
                        else:
                            if len(list(set(list(Cartline.objects.all().values_list('id', flat=True)))))>0:
                                max_id = max(list(set(list(Cartline.objects.all().values_list('id', flat=True)))))
                            else:
                                max_id = 0
                            cartproduct = Cartline.objects.create(id = max_id+1,
                                shoppingcartid=cart_obj, id_product=product_obj, num=1)
                            cart_obj.save()  
                    else:
                        if len(list(set(list(Shoppingcart.objects.all().values_list('id', flat=True)))))>0:
                            max_id = max(list(set(list(Shoppingcart.objects.all().values_list('id', flat=True)))))
                        else:
                            max_id = 0
                  
                        cart_obj =Shoppingcart.objects.create(id= max_id+1,customerid = customer)
                        self.request.session['cart_id'] = cart_obj.id

                        if len(list(set(list(Cartline.objects.all().values_list('id', flat=True)))))>0:
                            max_id = max(list(set(list(Cartline.objects.all().values_list('id', flat=True)))))
                        else:
                            max_id = 0
                        cartproduct = Cartline.objects.create(id = max_id+1,
                            shoppingcartid=cart_obj, id_product=product_obj, num=1)
                        cart_obj.save()
                return redirect("mycart")

class MyCartView(EcomMixin, LoginRequiredMixin,TemplateView):
    template_name = "app_cart/mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and Customer.objects.filter(id = self.request.user.id).exists():
            cart_id = self.request.session.get("cart_id", None)
            if cart_id:
                cart = Shoppingcart.objects.get(id=cart_id)
            else:
                customer = Customer.objects.get(id = self.request.user.id)
                if Shoppingcart.objects.filter(customerid = customer).exists():
                    cart = Shoppingcart.objects.get(customerid = customer)
                else:
                    if len(list(set(list(Shoppingcart.objects.all().values_list('id', flat=True)))))>0:
                        max_id = max(list(set(list(Shoppingcart.objects.all().values_list('id', flat=True)))))
                    else:
                        max_id = 0
                    cart = Shoppingcart.objects.create(id= max_id+1,customerid = customer)
            cartline = Cartline.objects.filter(shoppingcartid = cart, is_active = True)
            context['cartline'] = cartline
            context['cart'] = cart
        return context

class ManageCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = Cartline.objects.get(id=cp_id, is_active =True)
        cart_obj = cp_obj.shoppingcartid

        if action == "inc":
            cp_obj.num += 1
            cp_obj.save()
            cart_obj.save()
        elif action == "dcr":
            cp_obj.num -= 1
            cp_obj.save()
            cart_obj.save()
            if cp_obj.num == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.save()
            cp_obj.is_active = False
            cp_obj.save()
        else:
            pass
        return redirect("mycart")

# Xóa toàn bộ sản phẩm trong giỏ
class EmptyCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        customer = Customer.objects.get(id = self.request.user.id)

        cart = Shoppingcart.objects.get(id=cart_id) if cart_id else Shoppingcart.objects.get(customerid =customer)
        # [cartline.delete() for cartline in Cartline.objects.filter(shoppingcartid = cart)]
        for cartline in Cartline.objects.filter(shoppingcartid = cart, is_active = True):
            cartline.is_active =  False
            cartline.save()
        cart.save()
        return redirect("mycart")
