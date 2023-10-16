from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


# Create your models here.
class SectionBaseModel(SingletonModel):
    title = models.CharField(max_length=255, verbose_name=_('Título'))
    subtitle = models.TextField(verbose_name=_('Subtítulo'))
    image = models.ImageField(upload_to='sections/', verbose_name=_('Imagen'))

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
        verbose_name = _('Sobre nosotros')
        verbose_name_plural = verbose_name


class AboutUsSectionPerks(models.Model):
    about_us_section = models.ForeignKey(AboutUsSection, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name=_('Título'), null=True, blank=True, help_text=_('Opcional'))
    text = models.TextField(verbose_name=_('Text'), null=True, blank=True, help_text=_('Opcional'))
    image = models.ImageField(upload_to='sections/about us/', verbose_name=_('Imagen'), null=True, blank=True,
                              help_text=_('Opcional'))

    def __str__(self):
        return str(_('About Us Perk'))

    class Meta:
        verbose_name = _('About Us Section Perk')
        verbose_name_plural = _('About Us Section Perks')


class ProductsPortfolioSection(SectionBaseModel):
    class Meta:
        verbose_name = _('Productos del portafolio')
        verbose_name_plural = _('Productos del portafolio')


class WorksPortfolioSection(SectionBaseModel):
    class Meta:
        verbose_name = _('Portafolio de trabajo')
        verbose_name_plural = _('Portafolios de trabajos')


class WorkWithUsSection(SectionBaseModel):
    class Meta:
        verbose_name = _('Trabaja con nosotros')
        verbose_name_plural = _('Trabaja con nosotros')


class ContactUsSection(SectionBaseModel):
    class Meta:
        verbose_name = _('Contáctenos ')
        verbose_name_plural = _('Contáctenos')


class SellProductsSection(SectionBaseModel):
    class Meta:
        verbose_name = _('Producto de venta')
        verbose_name_plural = _('Productos en venta')
