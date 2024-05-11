# Generated by Django 5.0.3 on 2024-05-05 18:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apibankapp', '0002_alter_accountmodel_fk_id_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountmodel',
            name='FK_Id_customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='AccountType', to='apibankapp.customermodel'),
        ),
    ]
