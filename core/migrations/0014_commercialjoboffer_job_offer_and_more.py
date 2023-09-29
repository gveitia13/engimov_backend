# Generated by Django 4.2.3 on 2023-08-21 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_commercialjoboffer_joboffer_jobofferpool'),
    ]

    operations = [
        migrations.AddField(
            model_name='commercialjoboffer',
            name='job_offer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.joboffer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='commercialjoboffer',
            name='others',
            field=models.TextField(blank=True, null=True, verbose_name='Other Data'),
        ),
        migrations.AlterField(
            model_name='commercialjoboffer',
            name='sector',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Sector'),
        ),
        migrations.AlterField(
            model_name='commercialjoboffer',
            name='tel',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='jobofferpool',
            name='experience',
            field=models.TextField(blank=True, null=True, verbose_name='Experience'),
        ),
        migrations.AlterField(
            model_name='jobofferpool',
            name='formation',
            field=models.TextField(blank=True, null=True, verbose_name='Formation'),
        ),
        migrations.AlterField(
            model_name='jobofferpool',
            name='others',
            field=models.TextField(blank=True, null=True, verbose_name='Other Data'),
        ),
        migrations.AlterField(
            model_name='jobofferpool',
            name='skills',
            field=models.TextField(blank=True, null=True, verbose_name='Skills'),
        ),
        migrations.AlterField(
            model_name='jobofferpool',
            name='tel',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Phone Number'),
        ),
    ]