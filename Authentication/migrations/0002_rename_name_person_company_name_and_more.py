# Generated by Django 5.1.6 on 2025-02-10 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='name',
            new_name='company_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='person',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='owner_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='phone_number_1',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='person',
            name='phone_number_2',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
