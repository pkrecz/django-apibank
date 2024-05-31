# Generated by Django 5.0.3 on 2024-05-31 16:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apibankapp', '0028_alter_accountmodel_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountmodel',
            name='percent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
