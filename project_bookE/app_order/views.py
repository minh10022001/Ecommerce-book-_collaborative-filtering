from django.shortcuts import render
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from app_store.models import *
from app_cart.models import *
from app_cart.views import *
from app_user.models import *
from app_staff.models import OrderHistoryLog
from .models import *
from .forms  import *
from django.db.models import Q
# import datetime
import datetime
from datetime import timedelta
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
# from forex_python.converter import CurrencyRates
import uuid
# Create your views here.

class CheckoutView(EcomMixin, CreateView , LoginRequiredMixin):
    template_name = "app_order/checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user):
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        customer = Customer.objects.get(id = self.request.user.id)
        cart_obj = Shoppingcart.objects.get(id=cart_id) if cart_id else Shoppingcart.objects.get(customerid =customer)
        context['cart'] = cart_obj
        return context
       
    def form_valid(self,form):
        cart_id = self.request.session.get("cart_id")
        customer =Customer.objects.get(id= self.request.user.id)
        cart_obj = Shoppingcart.objects.get(id=cart_id) if cart_id else Shoppingcart.objects.get(customerid =customer)
        cartlines = cart_obj.cartline_set.all()
        
        method_payment = form.cleaned_data.get("paymentMethod")
        method_shipping = form.cleaned_data.get("shippingmethod")
        convert ={"1": "Thanh toán sau khi nhận hàng",
                    "2": "Thanh toán PayPal",
                    }
        convert_shipping ={"1": "Giao hàng tiêu chuẩn",
                    "2": "Giao hàng nhanh",
        }
        customershippingaddress  =form.cleaned_data.get("customershippingaddress")
        if len(list(set(list(Payment.objects.all().values_list('id', flat=True)))))>0:
            max_id_shipping = max(list(set(list(Payment.objects.all().values_list('id', flat=True)))))
        else:
            max_id_shipping  = 0
      
        if convert_shipping[method_shipping]  == "Giao hàng tiêu chuẩn":
            price_shipping = 10000
            dday = 2
        else:
            price_shipping = 20000
            dday = 5
        shipping =  Shipping.objects.create(id = max_id_shipping+1,price_shipping = price_shipping,address  = customershippingaddress, method = convert_shipping[method_shipping] ,date_shipping = datetime.datetime.now() +  timedelta(days=dday))
        
        if len(list(set(list(Payment.objects.all().values_list('id', flat=True)))))>0:
            max_id_payment = max(list(set(list(Payment.objects.all().values_list('id', flat=True)))))
        else:
            max_id_payment = 0

        if cart_obj.total >= 500000:
            amount = cart_obj.total
        else:
            amount = cart_obj.total+price_shipping
        payment = Payment.objects.create(id= max_id_payment +1,isComplete = False, time = None, method = convert[method_payment],id_cart  = cart_obj, amount =  amount ,id_shipping =  shipping)
        
        if len(list(set(list(Order.objects.all().values_list('id', flat=True)))))>0:
            max_id = max(list(set(list(Order.objects.all().values_list('id', flat=True)))))
        else:
            max_id = 0

        order =  Order.objects.create(id = max_id+1 ,paymentid = payment, customerid = customer,shippingid = shipping,time = datetime.datetime.now(),status = "Chờ xác nhận")
        if len(list(set(list(OrderHistoryLog.objects.all().values_list('id', flat=True)))))>0:
            max_id_log = max(list(set(list(OrderHistoryLog.objects.all().values_list('id', flat=True)))))
        else:
            max_id_log = 0
        orderlog = OrderHistoryLog.objects.create(id= max_id_log+1,id_order = order.id, status_current = order.status,action_by_type_user ='customer',id_user = order.customerid.id,date_modifided= datetime.datetime.now())
        for cartline in cartlines:
            if cartline.is_active == True:
                if len(list(set(list(Orderitem.objects.all().values_list('id', flat=True)))))>0:
                    max_id = max(list(set(list(Orderitem.objects.all().values_list('id', flat=True)))))
                else:
                    max_id = 0
                orderitem = Orderitem.objects.create(id = max_id+1,orderid = order, product = cartline.id_product, count = cartline.num,cartline= cartline)
                orderitem.save()
                cartline.is_order =  True
                cartline.is_active = False
                cartline.save()
        if convert[method_payment] == "Thanh toán sau khi nhận hàng":
            messages.success(self.request,"Đặt hàng thành thông")
            context = {'ord_obj':order}
        #     return redirect('home')
            return render(self.request, 'app_order/orderdetail.html', context)
        else:
            return redirect('paymentpaypal')



def paymentpaypal(request):
    customer =  Customer.objects.get(id = request.user.id)
    order = Order.objects.filter(customerid = customer).order_by('-id')[0]
    amount =  order.paymentid.amount
    usd_amount = amount *0.000041
    order_name  = "Order"+ str(order.id)
  
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(usd_amount),
        'item_name': order_name,
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('paypal-return')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('paypal-cancel')),
    }
    form =  PayPalPaymentsForm(initial = paypal_dict)
    context = {'form': form, 'customer':customer,'amount':int(amount),'usd_amount':usd_amount }
    return render(request, 'app_order/payment_paypal.html', context)
        
def paypal_return(request):
    customer =  Customer.objects.get(id = request.user.id)
    order = Order.objects.filter(customerid = customer).order_by('-id')[0]
    payment =  order.paymentid 
    payment.isComplete = True
    payment.time = datetime.datetime.now()
    payment.save()
    order.save()
  
    messages.success(request,"Đặt hàng thành thông")
    context = {'ord_obj':order}
    return render(request, 'app_order/orderdetail.html', context)

    
def paypal_cancel(request):
    customer =  Customer.objects.get(id = request.user.id)
    order = Order.objects.filter(customerid = customer).order_by('-id')[0]
    order.status = 'Đơn hàng đã bị huỷ'
    order.save()
    if len(list(set(list(OrderHistoryLog.objects.all().values_list('id', flat=True)))))>0:
        max_id_log = max(list(set(list(OrderHistoryLog.objects.all().values_list('id', flat=True)))))
    else:
        max_id_log = 0
    orderlog =  OrderHistoryLog.objects.create(id= max_id_log+1,id_order = order.id, status_current = 'Đơn hàng đã bị huỷ', action_by_type_user = 'customer',id_user = order.customerid.id, date_modifided= datetime.datetime.now())
    messages.error(request,"Đơn hàng bị hủy do chưa thanh toán PayPal")
    context = {'ord_obj':order}
    return render(request, 'app_order/orderdetail.html', context)

class MyOrdersView(TemplateView, LoginRequiredMixin):
    template_name = "app_order/myorders.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cus_id = kwargs['cus_id']
        kw = self.request.GET.get("keyword")
        customer = Customer.objects.get(id = cus_id)
        context['customer'] = customer
        if kw is not None:
            orders = Order.objects.filter (Q(id__icontains=kw))
        else:
            orders = Order.objects.filter(customerid=customer).order_by("-id")
        if len(orders) == 0:
            orders = None
        context["orders"] = orders
        context['account'] =  customer
        return context

class CustomerOrderDetailView(DetailView,LoginRequiredMixin):
    template_name = "app_order/orderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(id = request.user.id).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.id != order.customerid.id:
                return redirect("myorder")
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)