# Generated by Django 4.2.3 on 2023-09-30 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_commercialjoboffer_is_checked_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='joboffer',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is active'),
        ),
    ]