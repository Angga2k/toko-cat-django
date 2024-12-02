from django import forms
from .models import Purchase, Sales

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier', 'product', 'purchase_quantity']  # Gunakan nama field sesuai model

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['sales_quantity']
