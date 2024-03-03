from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', views.ProductCategoryView.as_view(), name='products_by_category'),
    path("product/<slug:slug>/", views.ProductDetailView.as_view(), name="productdetail"),
    path("myrating/<int:cus_id>/", views.MyRatingView.as_view(), name="myrating"),
    path("update-wishlist-<int:pro_id>/", views.UpdateToWishList.as_view(), name="updateWishList"),
    path("wishlist/", views.WishListView.as_view(), name="wishlist"),

    # path('admin-home/', views.AdminHomeView.as_view(), name= 'adminhome'),
    # path("admin-pending-orders/", views.AdminPendingOrder.as_view(), name='adminpendingorders'),
    # path("admin-all-orders/", views.AdminOrderListView.as_view(), name="adminorderlist"),
    # path("admin-product/list/", views.AdminProductListView.as_view(),name="adminproductlist"),
    # path("admin-import/import/<slug:slug>", views.AdminImportView.as_view(),name="adminimport"),
    # path("admin-import/list/", views.AdminImportListView.as_view(),name="adminimportlist"),
    # path("admin-user/list/", views.AdminUserListView.as_view(),name="adminuserlist"),
    # path("admin-product/add/<int:cate_id>/", views.AdminProductCreateView.as_view(),name="adminproductcreate"),
    # path("admin-product/delete-<int:pro_id>", views.AdminProductDeleteView.as_view(),name="adminproductdelete"),
    # path("admin-product-detail/<int:pro_id>/", views.AdminProductDetailView.as_view(), name="adminproductdetail"),
    # path("admin-user/disable/<int:user_id>/", views.AdminUserDisableView.as_view(), name="adminuserdisable"),
    # path("admin-user/enable/<int:user_id>/", views.AdminUserEnableView.as_view(), name="adminuserenable"),
    # path("admin/orderdetail/<int:pk>/", views.AdminOrderDetailView.as_view(), name = 'adminorderdetail'),
    # path("admin/changeorder/<int:pk>/",views.AdminOrderStatusChangeView.as_view(), name="adminorderstatuschange"),
    #  path("admin-dashboard/", views.AdminDashboardView.signed_public_dashboard, name="admindashboard"),
    
    
]

