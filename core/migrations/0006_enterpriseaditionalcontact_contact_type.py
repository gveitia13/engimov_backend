# Generated by Django 4.1 on 2023-07-14 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_enterpriseaditionalcontact'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterpriseaditionalcontact',
            name='contact_type',
            field=models.CharField(choices=[('email', 'E-Mail'), ('tel', 'Phone')], default='email', max_length=255, verbose_name='Contact Type'),
            preserve_default=False,
        ),
    ]
