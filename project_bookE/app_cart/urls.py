from django.urls import path
from . import views


urlpatterns = [
    path("my-cart/", views.MyCartView.as_view(), name="mycart"),
    path("add-to-cart-<int:pro_id>/", views.AddToCartView.as_view(), name="addtocart"),
    path("manage-cart/<int:cp_id>/", views.ManageCartView.as_view(), name="managecart"),
     path("empty-cart/", views.EmptyCartView.as_view(), name="emptycart"),
]

