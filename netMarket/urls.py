"""
URL configuration for netMarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from market.views import ProductDetailView, ProductListView, register_user, create_product, admin_dashboard, login_user, \
    display_full_image, edit_product, add_to_cart_view, cart_view, remove_from_cart_view, submit_order_view
from django.contrib.auth.views import PasswordChangeView

from netMarket import settings

urlpatterns = [

    path('product/<str:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:product_id>/full-image/', display_full_image, name='display_full_image'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('', lambda request: redirect('products/'), name='redirect_to_products'),
    path('registration/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('create_product/', create_product, name='create_product'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('admin_panel/', admin_dashboard, name='admin_dashboard'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('add_to_cart/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('submit_order/', submit_order_view, name='submit_order'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart_view, name='remove_from_cart')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)