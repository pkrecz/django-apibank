# Generated by Django 5.0.3 on 2024-05-16 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apibankapp', '0009_rename_fk_id_account_operationmodel_id_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customermodel',
            old_name='Id_customer',
            new_name='id_customer',
        ),
    ]