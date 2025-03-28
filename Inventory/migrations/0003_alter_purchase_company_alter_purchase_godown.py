# Generated by Django 5.1.6 on 2025-03-11 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0002_alter_purchase_delivery_no_and_more'),
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='master.company'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='godown',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='godwons', to='master.godown'),
        ),
    ]
