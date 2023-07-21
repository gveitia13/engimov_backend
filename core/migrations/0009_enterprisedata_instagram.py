# Generated by Django 4.1 on 2023-07-21 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_enterprisedata_facebook_enterprisedata_twitter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprisedata',
            name='instagram',
            field=models.CharField(blank=True, help_text='Optional', max_length=500, null=True, verbose_name='Enterprise Instagram Page'),
        ),
    ]