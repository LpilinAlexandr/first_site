from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('resume', views.download, name='download'),
    path('down_link', views.run, name='down_link'),
    path('shop', views.shop_page, name='shop'),
    path('cart', views.cart_page, name='cart'),
    path('shop/<str:slug>/', views.get_product_page, name='product_url'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)












