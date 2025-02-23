"""
URL configuration for tokocat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from cat import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.index),
    path('products/', views.existed_products, name='products'),
    path('new_products/', views.new_products, name='new_products'),
    path('update_products/<int:pk>', views.product_update_stock, name='product_update_stock'),
    path('sales/create/', views.create_sales, name='create_sales'),
    path('api/products/', views.product_list_api, name='product_list_api'),
]