from django import forms
from .models import *
from app_user.models import *

METHOD =(
    ("1", "Thanh toán sau khi nhận hàng"),
    ("2", "Thanh toán PayPal")
)
METHOD_SHIPPING =(

     ("1", "Giao hàng tiêu chuẩn"),
    ("2", "Giao hàng nhanh"),

)
class CheckoutForm(forms.ModelForm):
    customershippingaddress = forms.ModelChoiceField(queryset= AddressShipping.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    paymentMethod = forms.CharField(label = "Payment Method", widget=forms.Select(choices=METHOD,attrs={'class': 'form-control'}))
    shippingmethod = forms.CharField(label = "Shipping Method", widget=forms.Select(choices=METHOD_SHIPPING,attrs={'class': 'form-control'}))
    class Meta:
        model = Order
        fields = ["customershippingaddress",
                  "paymentMethod", "shippingmethod"]
    def __init__(self,user, *args, **kwargs): 
        # user = kwargs.pop('user', None) # pop the 'user' from kwargs dictionary      
        customer = Customer.objects.get(id = user.id)
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['customershippingaddress'].queryset = AddressShipping.objects.filter(account =customer, is_active= True)