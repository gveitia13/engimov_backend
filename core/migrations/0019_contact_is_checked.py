# Generated by Django 4.2.3 on 2023-10-01 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_commercialjoboffer_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='is_checked',
            field=models.BooleanField(default=False, verbose_name='Is checked'),
        ),
    ]
