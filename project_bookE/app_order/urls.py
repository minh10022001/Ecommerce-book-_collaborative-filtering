from django.urls import path
from . import views


urlpatterns = [
     path("checkout/", views.CheckoutView.as_view(), name="checkout"),
     path("myorder/<int:cus_id>/", views.MyOrdersView.as_view(), name="myorder"),
     path("order-<int:pk>/", views.CustomerOrderDetailView.as_view(), name = 'customerorderdetail'),
     path('paymentpaypal', views.paymentpaypal, name = 'paymentpaypal'),
     path('paypal-return', views.paypal_return, name = 'paypal-return'),
     path('paypal-cancel', views.paypal_cancel, name = 'paypal-cancel'),
   
]


   