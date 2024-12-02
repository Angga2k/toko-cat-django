from django.contrib import admin
from .models import Product, Supplier, Purchase, DetailPurchase, Sales, DetailSales
# Register your models here.

admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Purchase)
admin.site.register(DetailPurchase)
admin.site.register(Sales)
admin.site.register(DetailSales)