# Generated by Django 4.2.3 on 2023-12-19 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_alter_deliveryprice_delivery_place_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='telefono_comprador',
            field=models.CharField(default='', max_length=200, verbose_name='Teléfono del comprador'),
            preserve_default=False,
        ),
    ]
