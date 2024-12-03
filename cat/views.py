from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from . import templates
from . import models
from .forms import PurchaseForm, SalesForm
from django.contrib import messages
from django.db import transaction
from datetime import datetime
from django.db.models import Q

# Create your views here.

def index(request):
    context = {
        'header' : 'Hello World',
        'user_authentication' : True
    }

    return render(request, 'test.html', context)

def existed_products(request):
    products = models.Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products/products.html', context)

def new_products(request) :
    return render(request, 'products/new_products.html')

def product_list_api(request):
    term = request.GET.get('term', '')  # Ambil parameter pencarian
    products = models.Product.objects.filter(product_name__icontains=term)[:10]  # Filter produk berdasarkan pencarian
    data = [
        {"id": product.product_id, "text": product.product_name, "volume" : product.volume, "price" : product.price} for product in products
    ]
    return JsonResponse({"results": data})

def get_product_details(request):
    product_id = request.GET.get('product_name')
    try:
        product = models.Product.objects.get(pk=product_id)
        data = {
            'volume': product.volume,
            'price': product.price,
        }
        return JsonResponse(data)
    except models.Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

def product_create(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        volume = request.POST.get('volume')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        safety_stock = request.POST.get('safety_stock')
        if product_name and volume and price and stock:
            models.Product.objects.create(
                product_name=product_name,
                volume=int(volume),
                price=int(price),
                stock=int(stock),
                safety_stock=int(safety_stock)
            )
            messages.success(request, "Product created successfully!")
            return redirect('product_list')
        else:
            messages.error(request, "All fields are required.")
    return render(request, 'products/new_products.html', {'form_action': 'Create'})

def product_update_stock(request, pk):
    product = get_object_or_404(models.Product, pk=pk)  # Ambil produk berdasarkan primary key
    suppliers = models.Supplier.objects.all()
    if request.method == 'POST':
        purchase_quantity = request.POST.get('purchase_quantity')
        supplier_id = request.POST.get('supplier')
        
        # Validasi input
        if purchase_quantity and int(purchase_quantity) > 0 and supplier_id:
            supplier = get_object_or_404(models.Supplier, pk=supplier_id)
            
            # Tambahkan stok produk
            product.stock += int(purchase_quantity)
            product.save()
            
            # Simpan data pembelian ke tabel Purchase
            models.Purchase.objects.create(
                purchase_date=datetime.now(),
                supplier=supplier,
                product=product,
                purchase_quantity=int(purchase_quantity)
            )
            
            messages.success(request, f"Stock for {product.product_name} updated successfully! Purchase recorded.")
            return redirect('product_list')
        else:
            messages.error(request, "All fields are required and purchase quantity must be a positive integer.")
    
    return render(request, 'products/products.html', {'product': product})

def create_sales(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')  # Mendapatkan jumlah produk
        
        # Validasi input
        if not product_id or not quantity:
            messages.error(request, "Data produk atau jumlah tidak valid.")
            return redirect('create_sales')

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Jumlah produk harus lebih dari nol.")

            # Mulai transaksi database
            with transaction.atomic():
                # Dapatkan produk
                product = get_object_or_404(models.Product, pk=product_id)

                # Validasi stok
                if product.stock < quantity:
                    raise ValueError(f"Stok tidak mencukupi untuk produk {product.name}.")

                # Buat catatan di Sales
                sales = models.Sales.objects.create(
                    sales_date=datetime.now(),
                    sales_quantity=quantity,  # Jumlah produk
                )

                # Buat detail penjualan
                models.DetailSales.objects.create(
                    sales=sales,
                    product=product,
                    quantity=quantity  # Tambahkan jumlah produk di detail
                )

                # Perbarui stok produk
                product.stock -= quantity
                product.save()

                messages.success(request, "Penjualan berhasil dicatat dan stok diperbarui!")
                return redirect('dashboard')
        except ValueError as ve:
            messages.error(request, str(ve))
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {str(e)}")

    products = models.Product.objects.all()
    return render(request, 'inventory/sales_form.html', {'products': products})

