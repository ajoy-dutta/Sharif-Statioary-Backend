# Generated by Django 5.1.6 on 2025-03-11 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='delivery_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='invoice_challan_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='order_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
