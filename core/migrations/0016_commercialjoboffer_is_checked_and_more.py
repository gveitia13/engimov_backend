# Generated by Django 4.2.3 on 2023-09-30 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_enterprisedata_doc_folleto_digital_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commercialjoboffer',
            name='is_checked',
            field=models.BooleanField(default=False, verbose_name='Is checked'),
        ),
        migrations.AddField(
            model_name='jobofferpool',
            name='is_checked',
            field=models.BooleanField(default=False, verbose_name='Is checked'),
        ),
    ]
