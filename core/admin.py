from django.contrib import admin
from .models import ProductCategory, WorkCategory, Product, Work, Testimonial, EnterpriseData, \
    EnterpriseAditionalContact, Contact, TermsOfUse, PrivacyPolicy, JobOffer, JobOfferPool, CommercialJobOffer
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


class WorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_image')
    list_filter = ('category',)
    search_fields = ('name',)
    inlines = [TestimonialInline]


class EnterpriseDataAdmin(SingletonModelAdmin):
    inlines = [EnterpriseAditionalContactInLine]
    fieldsets = [
        (_('Datos principales'), {'fields': ('enterprise_name', 'email', 'location', 'tel', 'city')}),
        (_('Documentos'), {'fields': ('doc_folleto_digital', 'doc_presentation',)}),
        (_('Redes sociales'), {'fields': ('facebook', 'twitter', 'youtube', 'instagram',)}),
    ]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject')
    search_fields = ('name', 'email', 'subject')


@admin.register(TermsOfUse)
class TermsOfUseAdmin(admin.ModelAdmin):
    list_display = ('version', 'effective_date')
    search_fields = ('version',)


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('version', 'effective_date')
    search_fields = ('version',)


class JobOfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class JobOfferPoolAdmin(admin.ModelAdmin):
    pass


class CommercialJobOfferAdmin(admin.ModelAdmin):
    pass


admin.site.register(CommercialJobOffer, CommercialJobOfferAdmin)
admin.site.register(JobOfferPool, JobOfferPoolAdmin)
admin.site.register(JobOffer, JobOfferAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(WorkCategory, WorkCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(EnterpriseData, EnterpriseDataAdmin)
