# Generated by Django 4.2.3 on 2023-11-05 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0005_termsandprivacypolice'),
    ]

    operations = [
        migrations.CreateModel(
            name='TropipayConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tpp_client_id', models.CharField(blank=True, max_length=255, null=True)),
                ('tpp_client_secret', models.CharField(blank=True, max_length=255, null=True)),
                ('tpp_client_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('tpp_client_password', models.CharField(blank=True, max_length=255, null=True)),
                ('tpp_url', models.URLField(blank=True, default='www.tropipay.com', null=True)),
                ('tpp_success_url', models.URLField(blank=True, null=True)),
                ('tpp_failed_url', models.URLField(blank=True, null=True)),
                ('tpp_notification_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Configuración de Tropipay',
            },
        ),
    ]
