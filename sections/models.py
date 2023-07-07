from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class SectionBaseModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    subtitle = models.CharField(max_length=255, verbose_name=_('Subtitle'))
    image = models.ImageField(upload_to='sections/', verbose_name=_('Images'))

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        abstract = True

class IndexSection(SectionBaseModel):

    class Meta:
        verbose_name = _('Index')
        verbose_name_plural = _('Index')

class AboutUsSection(SectionBaseModel):

    class Meta:
        verbose_name = _('About Us')
        verbose_name_plural = _('About Us')

class ProductsPortfolioSection(SectionBaseModel):

    class Meta:
        verbose_name = _('Products Portfolio')
        verbose_name_plural = _('Products Portfolio')

class WorksPortfolioSection(SectionBaseModel):

    class Meta:
        verbose_name = _('Works Portfolio')
        verbose_name_plural = _('Works Portfolio')

class WorkWithUsSection(SectionBaseModel):

    class Meta:
        verbose_name = _('Work With Us')
        verbose_name_plural = _('Work With Us')

class ContactUsSection(SectionBaseModel):

    class Meta:
        verbose_name = _('Contact Us')
        verbose_name_plural = _('Contact Us')

class SellProductsSection(SectionBaseModel):

    class Meta:
        verbose_name = _('Sell Products')
        verbose_name_plural = _('Sell Products')