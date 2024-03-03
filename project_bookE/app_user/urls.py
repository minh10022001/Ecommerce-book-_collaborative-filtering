from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('forgotPassword/', views.forgotPassword, name='forgotPassword'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile_edit/<int:usr_id>/', views.EditProfileView.as_view(), name='profile_edit'),

    path("shipping_address/create/<int:cus_id>/", views.ShippingAddressCreateView.as_view(), name="shippingaddresscreate"),
    path("shipping_address/<int:cus_id>/", views.ShippingAddressListView.as_view(), name="shippingaddresslist"),
    path("shipping-address/edit/<int:cus_id>/<int:addr_id>/", views.ShippingAddressEditView.as_view(), name="shippingaddressedit"),
    path("shipping-address/delete/<int:cus_id>/<int:addr_id>/", views.ShippingAddressDeleteView.as_view(), name="shippingaddressdelete"),
    
]