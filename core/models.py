from django.db import models
from django.utils.translation import gettext_lazy as _

class ProductCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')

class WorkCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Work Category')
        verbose_name_plural = _('Works Categories')

class Product(models.Model):
    sku = models.CharField(unique=True, primary_key=True, max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,verbose_name=_('Category'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to='products/', verbose_name=_('Images'))
    price = models.FloatField(verbose_name=_('Price'))
    visibilidad = models.BooleanField(verbose_name=_('Visibility'))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

class Work(models.Model):
    category = models.ForeignKey(WorkCategory, on_delete=models.CASCADE, verbose_name=_('Category'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to='products/', verbose_name=_('Images'))

    class Meta:
        verbose_name = _('Work')
        verbose_name_plural = _('Works')

class Testimonial(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, verbose_name=_('Work'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    link = models.URLField(verbose_name=_('Link'), null=True, blank=True, help_text=_('Optional'))
    testimonial = models.TextField(verbose_name=_('Testimonial'))

    class Meta:
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')
