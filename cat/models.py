from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    volume = models.IntegerField()
    price = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.product_name

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=255)

    def __str__(self):
        return self.supplier_name

class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    purchase_date = models.DateTimeField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_quantity = models.IntegerField()

    def __str__(self):
        return f"Purchase {self.purchase_id} - {self.purchase_date}"

class DetailPurchase(models.Model):
    detail_purchase_id = models.AutoField(primary_key=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="details")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"DetailPurchase {self.detail_purchase_id}"

class Sales(models.Model):
    sales_id = models.AutoField(primary_key=True)
    sales_date = models.DateTimeField()
    sales_quantity = models.IntegerField()

    def __str__(self):
        return f"Sales {self.sales_id} - {self.sales_date}"

class DetailSales(models.Model):
    detail_sales_id = models.AutoField(primary_key=True)
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE, related_name="details")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"DetailSales {self.detail_sales_id}"