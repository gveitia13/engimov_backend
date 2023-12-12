from django.contrib import admin
from .models import ProductCategory, WorkCategory, Product, Work, Testimonial, EnterpriseData, \
    EnterpriseAditionalContact, Contact, TermsOfUse, PrivacyPolicy, JobOffer, JobOfferPool, CommercialJobOffer, \
    DeliveryPlace, DeliveryPrice
from solo.admin import SingletonModelAdmin
from django.utils.translation import gettext_lazy as _


class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 0


class JobOfferPoolInline(admin.TabularInline):
    model = JobOfferPool
    extra = 0


class EnterpriseAditionalContactInLine(admin.TabularInline):
    model = EnterpriseAditionalContact
    extra = 0


class DeliveryPriceInLine(admin.TabularInline):
    model = DeliveryPrice
    extra = 0


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class WorkCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'price', 'is_sale', 'visible')
    list_filter = ('category', 'visible', 'is_sale')
    search_fields = ('sku', 'name')
    list_editable = ('is_sale', 'visible')
    ordering = ('-visible', '-is_sale')
    list_per_page = 15
    fieldsets = [
        ('General', {
            'fields': [
                'sku', 'name', 'category', 'price', 'description', 'image'
            ],
        }),
        ('Opciones', {
            'fields': [
                'is_sale', 'visible', 'delivery_time', 'stock'
            ],
        })
    ]
    inlines = [DeliveryPriceInLine]


class WorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_image')
    list_filter = ('category',)
    search_fields = ('name',)
    fieldsets = [
        ('Datos principales', {'fields': ('name', 'category', 'image', 'description')}),
        ('Datos a traducir', {'fields': ('name_pt', 'description_pt', 'name_en', 'description_en')}),
    ]
    # inlines = [TestimonialInline]


class EnterpriseDataAdmin(SingletonModelAdmin):
    inlines = [EnterpriseAditionalContactInLine]
    fieldsets = [
        (_('Datos principales'), {'fields': ('enterprise_name', 'email', 'location', 'tel', 'city')}),
        (_('Documentos'), {'fields': ('doc_folleto_digital', 'doc_presentation',)}),
        (_('Redes sociales'), {'fields': ('facebook', 'twitter', 'youtube', 'instagram',)}),
    ]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_checked')
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_checked',)
    ordering = ('is_checked',)


class JobOfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_description', 'is_active')
    list_editable = ('is_active',)


class JobOfferPoolAdmin(admin.ModelAdmin):
    list_display = ('job_offer', 'name', 'email', 'cv', 'is_checked')
    list_editable = ('is_checked',)


class CommercialJobOfferAdmin(admin.ModelAdmin):
    list_display = ('job_offer', 'name', 'email', 'is_checked')
    list_editable = ('is_checked',)


admin.site.register(TermsOfUse, SingletonModelAdmin)
admin.site.register(PrivacyPolicy, SingletonModelAdmin)
admin.site.register(CommercialJobOffer, CommercialJobOfferAdmin)
admin.site.register(JobOfferPool, JobOfferPoolAdmin)
admin.site.register(JobOffer, JobOfferAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(WorkCategory, WorkCategoryAdmin)
admin.site.register(DeliveryPlace, WorkCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(EnterpriseData, EnterpriseDataAdmin)
