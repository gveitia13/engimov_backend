# Generated by Django 4.1 on 2023-07-07 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_workcategory_alter_productcategory_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='visibilidad',
            new_name='visible',
        ),
    ]
