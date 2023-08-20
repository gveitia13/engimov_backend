# Generated by Django 4.1 on 2023-08-20 12:37

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_privacypolicy_termsofuse'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommercialJobOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('tel', models.CharField(max_length=255, verbose_name='Phone Number')),
                ('sector', models.CharField(max_length=255, verbose_name='Sector')),
                ('business_offer', models.TextField(verbose_name='Business Offer')),
                ('others', models.TextField(verbose_name='Other Data')),
            ],
            options={
                'verbose_name': 'Commercial Job Offer',
                'verbose_name_plural': 'Commercial Job Offers',
            },
        ),
        migrations.CreateModel(
            name='JobOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', ckeditor.fields.RichTextField(max_length=400, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Job Offer',
                'verbose_name_plural': 'Job Offers',
            },
        ),
        migrations.CreateModel(
            name='JobOfferPool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('tel', models.CharField(max_length=255, verbose_name='Phone Number')),
                ('formation', models.TextField(verbose_name='Formation')),
                ('cv', models.FileField(upload_to='cv/', verbose_name='CV')),
                ('experience', models.TextField(verbose_name='Experience')),
                ('skills', models.TextField(verbose_name='Skills')),
                ('others', models.TextField(verbose_name='Other Data')),
                ('job_offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.joboffer')),
            ],
            options={
                'verbose_name': 'Job Offer Pool',
                'verbose_name_plural': 'Job Offers Pools',
            },
        ),
    ]
