from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


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
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name=_('Category'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to='products/', verbose_name=_('Images'))
    price = models.FloatField(verbose_name=_('Price'))
    visible = models.BooleanField(verbose_name=_('Visibility'))
    is_sale = models.BooleanField(_('En venta'), default=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Work(models.Model):
    category = models.ForeignKey(WorkCategory, on_delete=models.CASCADE, verbose_name=_('Category'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to='works/', verbose_name=_('Images'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Work')
        verbose_name_plural = _('Works')


class Testimonial(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, verbose_name=_('Work'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    link = models.URLField(verbose_name=_('Link'), null=True, blank=True, help_text=_('Optional'))
    testimonial = models.TextField(verbose_name=_('Testimonial'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')


class EnterpriseData(SingletonModel):
    enterprise_name = models.CharField(max_length=255, verbose_name=_('Enterprise Name'))
    location = models.TextField(verbose_name=_('Enterprise Google Maps Location'))
    email = models.EmailField(verbose_name=_('Enterprise Main Email'))
    tel = models.CharField(max_length=255, verbose_name=_('Enterprise Main Phone Number'))
    address = models.TextField(verbose_name=_('Enterprise Address'))
    city = models.CharField(_('City'), max_length=250, null=True, blank=True, help_text=_('Optional'))
    facebook = models.CharField(max_length=500, verbose_name=_('Enterprise Facebook Page'), null=True, blank=True,
                                help_text=_('Optional'))
    twitter = models.CharField(max_length=500, verbose_name=_('Enterprise Twitter Page'), null=True, blank=True,
                               help_text=_('Optional'))
    youtube = models.CharField(max_length=500, verbose_name=_('Enterprise Youtube Page'), null=True, blank=True,
                               help_text=_('Optional'))
    instagram = models.CharField(max_length=500, verbose_name=_('Enterprise Instagram Page'), null=True, blank=True,
                                 help_text=_('Optional'))

    def __str__(self):
        return "{}".format(self.enterprise_name)

    class Meta:
        verbose_name = _('Enterprise Information')
        verbose_name_plural = _('Enterprise Information')


class EnterpriseAditionalContact(models.Model):
    ENTERPRISE_CONTACT_CHOICES = (
        ('email', _('E-Mail')),
        ('tel', _('Phone')),
    )
    enterprise = models.ForeignKey(EnterpriseData, on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=255, verbose_name=_('Contact Type'), choices=ENTERPRISE_CONTACT_CHOICES)
    contact = models.CharField(max_length=255, verbose_name=_('Contact'))
    contact_aditional_info = models.CharField(max_length=255, verbose_name=_('Contact Aditional Info'), null=True,
                                              blank=True, help_text=_('Optional'))

    def __str__(self):
        return '{}'.format(self.contact)

    class Meta:
        verbose_name = _('Enterprise Aditional Contact')
        verbose_name_plural = _('Enterprise Aditional Contacts')


class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    subject = models.CharField(max_length=255, verbose_name=_('Subject'))
    text = models.TextField(verbose_name=_('Text'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
