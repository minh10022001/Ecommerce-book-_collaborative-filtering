from django.contrib import admin
from django.urls import path
from django.urls import path, include
# from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.home, name='home'),
    path("", include("app_store.urls")),
    path('accounts/', include('app_user.urls')),
    path('store/', include('app_store.urls')),
    path('cart/', include('app_cart.urls')),
    path('order/', include('app_order.urls')),
    path('admin_staff/', include('app_staff.urls')),
    path('paypal/', include('paypal.standard.ipn.urls'))
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
