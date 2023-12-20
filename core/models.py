import uuid as uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.forms import model_to_dict
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel
from ckeditor.fields import RichTextField

from engimovCaribe.utils import traducir_por_defecto


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


class DeliveryPlace(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    description = models.TextField('Descripción', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lugar de entrega'
        verbose_name_plural = 'Lugares de entrega'


class Product(models.Model):
    sku = models.CharField(unique=True, primary_key=True, max_length=255, default=uuid.uuid4,
                           help_text='Identificador único', )
    # sku = models.UUIDField(verbose_name='ID', primary_key=True, default=uuid.uuid4, editable=False,
    #                        help_text='Identificador único')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name=_('Categoría'))
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    description = models.TextField(verbose_name=_('Descripción'))
    image = models.ImageField(upload_to='products/', verbose_name=_('Imagen'))
    price = models.FloatField(verbose_name=_('Precio'),
                              validators=[MinValueValidator(0, 'Debe ser mayor que cero')])
    visible = models.BooleanField(verbose_name=_('Visibilidad'))
    is_sale = models.BooleanField(_('En venta'), default=False)
    stock = models.PositiveSmallIntegerField(verbose_name='Cantidad de inventario', default=1)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    delivery_time = models.PositiveSmallIntegerField('Tiempo de entrega (días)', default=2)

    # delivery_prices = models.ManyToManyField(DeliveryPlace, through='DeliveryPrice')

    # def save(self, *args, **kwargs):
    #     if not self.sku:
    #         # Generar un SKU aleatorio usando letras y dígitos
    #         self.sku = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Producto')
        verbose_name_plural = _('Productos')


class DeliveryPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    delivery_place = models.ForeignKey(DeliveryPlace, on_delete=models.CASCADE, verbose_name='Lugar de entrega')
    price = models.FloatField(verbose_name=_('Precio'), validators=[MinValueValidator(0, 'Debe ser mayor que cero')])

    def __str__(self):
        return f'{self.delivery_place} - {self.price} USD'

    class Meta:
        verbose_name = 'Precio de entrega'
        verbose_name_plural = 'Precios de entrega'


class Work(models.Model):
    category = models.ForeignKey(WorkCategory, on_delete=models.CASCADE, verbose_name=_('Categoría'))
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    description = models.TextField(verbose_name=_('Descripción'))
    image = models.ImageField(upload_to='works/', verbose_name=_('Imagen'),
                              help_text='Poner imagen horizontal, relación aspecto 16:9 preferiblemente')
    # Descripciones
    name_pt = models.CharField(max_length=255, verbose_name=_('Nombre Portugués'), null=True, blank=True,
                               help_text='Dejar este campo vacío hará que el sistema proponga una traducción '
                                         'automática. La traducción automática puede ser modificada.', )
    name_en = models.CharField(max_length=255, verbose_name=_('Nombre Inglés'), null=True, blank=True,
                               help_text='Dejar este campo vacío hará que el sistema proponga una traducción '
                                         'automática. La traducción automática puede ser modificada.', )
    description_pt = models.TextField('Descripción Portugués', null=True, blank=True,
                                      help_text='Dejar este campo vacío hará que el sistema proponga una traducción '
                                                'automática. La traducción automática puede ser modificada.', )
    description_en = models.TextField('Descripción Inglés', null=True, blank=True,
                                      help_text='Dejar este campo vacío hará que el sistema proponga una traducción '
                                                'automática. La traducción automática puede ser modificada.', )

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Trabajo')
        verbose_name_plural = _('Trabajos')

    def save(self, *args, **kwargs):
        try:
            if not self.description_en:
                self.description_en = traducir_por_defecto(self.description, 'en')
            if not self.description_pt:
                self.description_pt = traducir_por_defecto(self.description, 'pt')

        except:
            pass
        super().save()

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
    tropipay_impuesto = models.FloatField('Impuesto de Tropipay', default=3.45,
                                          help_text='Porciento del total de la orden aumentado',
                                          validators=[MinValueValidator(0, 'Debe ser mayor que cero')])
    checkout_allowed = models.BooleanField(default=True, verbose_name='Permitir compras',
                                           help_text='Permitir a los usuarios realizar compras')

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


class Orden(models.Model):
    link_de_pago = models.CharField(max_length=500, null=True, blank=True)
    total = models.FloatField(default=0, verbose_name='Importe total')
    precio_envio = models.FloatField(default=0, verbose_name='Precio de envío')
    # moneda = models.CharField(max_length=255, default='Euro')
    uuid = models.UUIDField(verbose_name='ID', primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField('Estado', choices=(
        ('1', 'Completada'),
        ('2', 'Pendiente'),
        ('3', 'Cancelada'),
    ), max_length=10, default='2')
    date_created = models.DateTimeField('Fecha', auto_now_add=True, )
    # Campos del form
    tiempo_de_entrega = models.PositiveIntegerField('Tiempo de entrega máximo')
    nombre = models.CharField('Nombre(s)', max_length=200)
    apellidos = models.CharField('Apellidos', max_length=200)
    telefono_comprador = models.CharField('Teléfono del comprador', max_length=200)
    correo = models.EmailField('Correo del comprador')
    detalles_direccion = models.TextField('Detalles de dirección', null=True, blank=True)

    def __str__(self):
        return '{}'.format(str(self.uuid))

    def get_total(self):
        return '{:.2f}'.format(self.total)

    def get_componente(self):
        return mark_safe(''.join(['•' + i.__str__() + '<br>' for i in self.componente_orden.all()]))

    def get_cancel_link(self):
        if self.status != '3':
            return mark_safe(
                f'<a href="{reverse_lazy("cancelar", kwargs={"pk": self.pk})}" class="btn btn-danger rounded-pill '
                f'">Cancelar<a/>')
        else:
            return ''

    get_total.short_description = 'Importe total'
    get_cancel_link.short_description = 'Opciones'
    get_componente.short_description = 'Componentes'

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'
        ordering = ('-date_created', '-status',)

    def toJSON(self):
        item = model_to_dict(self)
        item['date_created'] = self.date_created.strftime('%d-%m-%Y')
        item['uuid'] = str(self.uuid)
        item['componentes'] = [i.toJSON() for i in self.componente_orden.all()]
        return item


class ComponenteOrden(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='componente_producto')
    respaldo = models.FloatField()
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='componente_orden')
    cantidad = models.IntegerField()

    def __str__(self):
        try:
            return '{}x {} - {} {}'.format(self.cantidad, self.producto.name, '{:.2f}'.format(self.respaldo),
                                           'USD')
        except:
            return '{}x {} - {} {}'.format(self.cantidad, "ERROR", '{:.2f}'.format(self.respaldo),
                                           'USD')

    def Componente(self):
        return str(self)

    def toJSON(self):
        item = model_to_dict(self, exclude=['orden'])
        return item

    class Meta:
        ordering = ('orden', 'producto')
        verbose_name = 'Componente de orden'
        verbose_name_plural = 'Componentes de ordenes'
