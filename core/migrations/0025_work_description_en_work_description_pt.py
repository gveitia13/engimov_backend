# Generated by Django 4.2.3 on 2023-11-11 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_remove_testimonial_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='work',
            name='description_pt',
            field=models.TextField(blank=True, null=True),
        ),
    ]
