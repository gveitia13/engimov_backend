from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel
from ckeditor.fields import RichTextField


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
    image = models.ImageField(upload_to='works/', verbose_name=_('Images'),
                              help_text='Poner imagen horizontal, relación aspecto 16:9 preferiblemente')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Work')
        verbose_name_plural = _('Works')

    def get_image(self):
        return mark_safe(f'<img src="{self.image.url}" class="img-fluid" width=65/>')

    get_image.short_description = 'Imagen'


class JobOffer(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = RichTextField(max_length=400, verbose_name=_('Description'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Job Offer')
        verbose_name_plural = _('Job Offers')


class JobOfferPool(models.Model):
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    tel = models.CharField(max_length=255, verbose_name=_('Phone Number'), null=True, blank=True)
    formation = models.TextField(verbose_name=_('Formation'), null=True, blank=True)
    cv = models.FileField(upload_to='cv/', storage=None, verbose_name=_('CV'))
    experience = models.TextField(verbose_name=_('Experience'), null=True, blank=True)
    skills = models.TextField(verbose_name=_('Skills'), null=True, blank=True)
    others = models.TextField(verbose_name=_('Other Data'), null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Job Offer Pool')
        verbose_name_plural = _('Job Offers Pools')


class CommercialJobOffer(models.Model):
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    tel = models.CharField(max_length=255, verbose_name=_('Phone Number'), null=True, blank=True)
    sector = models.CharField(max_length=255, verbose_name=_('Sector'), null=True, blank=True)
    business_offer = models.TextField(verbose_name=_('Business Offer'))
    others = models.TextField(verbose_name=_('Other Data'), null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Commercial Job Offer')
        verbose_name_plural = _('Commercial Job Offers')


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
    doc_folleto_digital = models.FileField(_('Folleto digital'), null=True, blank=True, upload_to='doc/')
    doc_presentation = models.FileField(_('Carta de presentación'), null=True, blank=True, upload_to='doc/')

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


class TermsOfUse(SingletonModel):
    version = models.CharField(max_length=255, verbose_name=_('Version'))
    content = models.TextField(verbose_name=_('Content'))
    effective_date = models.DateField(verbose_name=_('Effective Date'))

    def __str__(self):
        return '{} - {}'.format(self.version, self.effective_date)

    class Meta:
        verbose_name = _('Terms of Use')
        verbose_name_plural = _('Terms of Use')


class PrivacyPolicy(SingletonModel):
    version = models.CharField(max_length=255, verbose_name=_('Version'))
    content = models.TextField(verbose_name=_('Content'))
    effective_date = models.DateField(verbose_name=_('Effective Date'))

    def __str__(self):
        return '{} - {}'.format(self.version, self.effective_date)

    class Meta:
        verbose_name = _('Privacy Policy')
        verbose_name_plural = _('Privacy Policies')
