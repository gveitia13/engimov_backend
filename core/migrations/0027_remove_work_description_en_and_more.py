# Generated by Django 4.2.3 on 2023-11-12 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_work_name_en_work_name_pt_alter_work_description_en_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='work',
            name='description_pt',
        ),
        migrations.RemoveField(
            model_name='work',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='work',
            name='name_pt',
        ),
    ]