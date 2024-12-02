# Generated by Django 5.1.3 on 2024-12-02 08:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('volume', models.IntegerField()),
                ('price', models.IntegerField()),
                ('stock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('sales_id', models.AutoField(primary_key=True, serialize=False)),
                ('sales_date', models.DateTimeField()),
                ('sales_quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('supplier_id', models.AutoField(primary_key=True, serialize=False)),
                ('supplier_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('purchase_id', models.AutoField(primary_key=True, serialize=False)),
                ('purchase_date', models.DateTimeField()),
                ('purchase_quantity', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cat.product')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cat.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='DetailPurchase',
            fields=[
                ('detail_purchase_id', models.AutoField(primary_key=True, serialize=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cat.product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='cat.purchase')),
            ],
        ),
        migrations.CreateModel(
            name='DetailSales',
            fields=[
                ('detail_sales_id', models.AutoField(primary_key=True, serialize=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cat.product')),
                ('sales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='cat.sales')),
            ],
        ),
    ]