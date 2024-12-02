from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . import templates
from . import models
from .forms import PurchaseForm, SalesForm
from django.contrib import messages

# Create your views here.

def index(request):
    context = {
        'header' : 'Hello World',
        'user_authentication' : True
    }

    return render(request, 'test.html', context)

def new_products(request):
    return render(request, 'products/products.html')

def existed_products(request) :
    return render(request, 'products/new_products.html')

def product_create(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        volume = request.POST.get('volume')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        if product_name and volume and price and stock:
            models.Product.objects.create(
                product_name=product_name,
                volume=int(volume),
                price=int(price),
                stock=int(stock),
            )
            messages.success(request, "Product created successfully!")
            return redirect('product_list')
        else:
            messages.error(request, "All fields are required.")
    return render(request, 'products/product_form.html', {'form_action': 'Create'})

# Update Product
def product_update(request, pk):
    product = get_object_or_404(models.Product, pk=pk)
    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.volume = request.POST.get('volume')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        if product.product_name and product.volume and product.price and product.stock:
            product.save()
            messages.success(request, "Product updated successfully!")
            return redirect('product_list')
        else:
            messages.error(request, "All fields are required.")
    return render(request, 'products/product_form.html', {'product': product, 'form_action': 'Update'})

# Delete Product
def product_delete(request, pk):
    product = get_object_or_404(models.Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

def create_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pembelian berhasil dicatat!")
            return redirect('dashboard')
    else:
        form = PurchaseForm()
    return render(request, 'purchase/purchase.html', {'form': form})

def create_sales(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Penjualan berhasil dicatat!")
                return redirect('dashboard')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = SalesForm()
    return render(request, 'inventory/sales_form.html', {'form': form})