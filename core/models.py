from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel
from ckeditor.fields import RichTextField


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Categoría de producto')
        verbose_name_plural = _('Categorías de productos')


class WorkCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Categoría de trabajos')
        verbose_name_plural = _('Categorías de trabajos')


class Product(models.Model):
    sku = models.CharField(unique=True, primary_key=True, max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name=_('Categoría'))
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    description = models.TextField(verbose_name=_('Descripción'))
    image = models.ImageField(upload_to='products/', verbose_name=_('Imagen'))
    price = models.FloatField(verbose_name=_('Precio'))
    visible = models.BooleanField(verbose_name=_('Visibilidad'))
    is_sale = models.BooleanField(_('En venta'), default=False)
    stock = models.IntegerField(verbose_name='Cantidad de inventario', default=1)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Producto')
        verbose_name_plural = _('Productos')


class Work(models.Model):
    category = models.ForeignKey(WorkCategory, on_delete=models.CASCADE, verbose_name=_('Categoría'))
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    description = models.TextField(verbose_name=_('Descripción'))
    image = models.ImageField(upload_to='works/', verbose_name=_('Imagen'),
                              help_text='Poner imagen horizontal, relación aspecto 16:9 preferiblemente')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Trabajo')
        verbose_name_plural = _('Trabajos')

    def get_image(self):
        return mark_safe(f'<img src="{self.image.url}" class="img-fluid" width=65/>')

    get_image.short_description = 'Imagen'


class JobOffer(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    description = RichTextField(max_length=400, verbose_name=_('Descripción'))
    is_active = models.BooleanField(_('Está Activo'), default=True)

    def get_description(self):
        return mark_safe(self.description)

    get_description.short_description = _('Descripción')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Oferta de trabajo')
        verbose_name_plural = _('Ofertas de trabajos')
        ordering = ('is_active', '-pk')


class JobOfferPool(models.Model):
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    email = models.EmailField(verbose_name=_('Email'))
    tel = models.CharField(max_length=255, verbose_name=_('Número de teléfono'), null=True, blank=True)
    formation = models.TextField(verbose_name=_('Formación'), null=True, blank=True)
    cv = models.FileField(upload_to='cv/', verbose_name=_('CV'))
    experience = models.TextField(verbose_name=_('Experiencia'), null=True, blank=True)
    skills = models.TextField(verbose_name=_('habilidades'), null=True, blank=True)
    others = models.TextField(verbose_name=_('Otros datos'), null=True, blank=True)
    is_checked = models.BooleanField(_('Está revisada'), default=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Cantera de oferta de trabajo')
        verbose_name_plural = _('Canteras de ofertas de trabajos')
        ordering = ('is_checked', 'job_offer', 'pk')


class CommercialJobOffer(models.Model):
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    email = models.EmailField(verbose_name=_('Email'))
    tel = models.CharField(max_length=255, verbose_name=_('Número de teléfomo'), null=True, blank=True)
    sector = models.CharField(max_length=255, verbose_name=_('Sector'), null=True, blank=True)
    business_offer = models.TextField(verbose_name=_('Oferta de negocio'))
    others = models.TextField(verbose_name=_('Otros datos'), null=True, blank=True)
    is_checked = models.BooleanField(_('Está revisada'), default=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Oferta de trabajo comercial')
        verbose_name_plural = _('Ofertas de trabajos comerciales')
        ordering = ('is_checked', 'job_offer', '-pk')


class Testimonial(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, verbose_name=_('Trabajos'))
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    link = models.URLField(verbose_name=_('Link'), null=True, blank=True, help_text=_('Opcional'))
    testimonial = models.TextField(verbose_name=_('Testimonios'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Testimonio')
        verbose_name_plural = _('Testimonios')


class EnterpriseData(SingletonModel):
    enterprise_name = models.CharField(max_length=255, verbose_name=_('Nombre de empresa'))
    location = models.TextField(verbose_name=_('Localizción de google maps de la Emppresa'))
    email = models.EmailField(verbose_name=_('Correo principal de la emresa'))
    tel = models.CharField(max_length=255, verbose_name=_('Teléfono principal de la empresa'), null=True, blank=True)
    address = models.TextField(verbose_name=_('Dirección de la empresa'))
    city = models.CharField(_('Ciudad'), max_length=250, null=True, blank=True, help_text=_('Opcional'))
    facebook = models.CharField(max_length=500, verbose_name=_('Página de Facebook de la empresa'), null=True,
                                blank=True,
                                help_text=_('Optional'))
    twitter = models.CharField(max_length=500, verbose_name=_('Página de Twitter de la empresa'), null=True, blank=True,
                               help_text=_('Optional'))
    youtube = models.CharField(max_length=500, verbose_name=_('Página de Youtube de la empresa'), null=True, blank=True,
                               help_text=_('Optional'))
    instagram = models.CharField(max_length=500, verbose_name=_('Página de instagram de la empresa'), null=True,
                                 blank=True,
                                 help_text=_('Opcional'))
    doc_folleto_digital = models.FileField(_('Folleto digital'), null=True, blank=True, upload_to='doc/')
    doc_presentation = models.FileField(_('Carta de presentación'), null=True, blank=True, upload_to='doc/')

    def __str__(self):
        return "{}".format(self.enterprise_name)

    class Meta:
        verbose_name = _('Información de la empresa')
        verbose_name_plural = _('Informaciónes de la empresa')


class EnterpriseAditionalContact(models.Model):
    ENTERPRISE_CONTACT_CHOICES = (
        ('email', _('E-Mail')),
        ('tel', _('Teléfono')),
    )
    enterprise = models.ForeignKey(EnterpriseData, on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=255, verbose_name=_('Tipo de contacto'),
                                    choices=ENTERPRISE_CONTACT_CHOICES)
    contact = models.CharField(max_length=255, verbose_name=_('Contacto'))
    contact_aditional_info = models.CharField(max_length=255, verbose_name=_('Info adicional'), null=True,
                                              blank=True, help_text=_('Opcional'))

    def __str__(self):
        return '{}'.format(self.contact)

    class Meta:
        verbose_name = _('Contacto adicional de la empresa')
        verbose_name_plural = _('Contactos adicionales de la empresa')


class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    email = models.EmailField(verbose_name=_('Email'))
    subject = models.CharField(max_length=255, verbose_name=_('Asunto'))
    text = models.TextField(verbose_name=_('Texto'))
    is_checked = models.BooleanField(_('Está revisada'), default=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Contacto')
        verbose_name_plural = _('Contactos')


class TermsOfUse(SingletonModel):
    version = models.CharField(max_length=255, verbose_name=_('Versión'))
    content = RichTextField(verbose_name=_('Contenido'))
    effective_date = models.DateField(verbose_name=_('Fecha de Efectividad'))

    def __str__(self):
        return '{} - {}'.format('Términos y Condiciones', self.effective_date)

    class Meta:
        verbose_name = _('Término de Uso')
        verbose_name_plural = _('Términos de Uso')


class PrivacyPolicy(SingletonModel):
    version = models.CharField(max_length=255, verbose_name=_('Version'))
    content = RichTextField(verbose_name=_('Contenido'))
    effective_date = models.DateField(verbose_name=_('Fecha de Efectividad'))

    def __str__(self):
        return '{} - {}'.format('Política de Privacidad', self.effective_date)

    class Meta:
        verbose_name = _('Política de privacidad')
        verbose_name_plural = _('Políticas de privacidad')
