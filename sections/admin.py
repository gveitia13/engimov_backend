from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import IndexSection, AboutUsSection, ProductsPortfolioSection, WorksPortfolioSection, WorkWithUsSection, \
    ContactUsSection, SellProductsSection, AboutUsSectionPerks
from solo.admin import SingletonModelAdmin

class AboutUsSectionPerksInline(admin.StackedInline):
    model = AboutUsSectionPerks
    extra = 0

class IndexSectionAdmin(SingletonModelAdmin):
    list_display = ('title', 'subtitle')
    search_fields = ('title', 'subtitle')

class AboutUsSectionAdmin(SingletonModelAdmin):
    list_display = ('title', 'subtitle')
    search_fields = ('title', 'subtitle')
    inlines = [AboutUsSectionPerksInline, ]

class ProductsPortfolioAdmin(SingletonModelAdmin):
    list_display = ('title', 'subtitle')
    search_fields = ('title', 'subtitle')

class WorksPortfolioAdmin(SingletonModelAdmin):
    list_display = ('title', 'subtitle')
    search_fields = ('title', 'subtitle')

class WorkWithUsAdmin(SingletonModelAdmin):
    list_display = ('title', 'subtitle')
    search_fields = ('title', 'subtitle')

class ContactUsAdmin(SingletonModelAdmin):
    list_display = ('title', 'subtitle')
    search_fields = ('title', 'subtitle')

class SellProductsAdmin(SingletonModelAdmin):
    list_display = ('title', 'subtitle')
    search_fields = ('title', 'subtitle')

admin.site.register(IndexSection, IndexSectionAdmin)
admin.site.register(AboutUsSection, AboutUsSectionAdmin)
admin.site.register(ProductsPortfolioSection, ProductsPortfolioAdmin)
admin.site.register(WorksPortfolioSection, WorksPortfolioAdmin)
admin.site.register(WorkWithUsSection, WorkWithUsAdmin)
admin.site.register(ContactUsSection, ContactUsAdmin)
admin.site.register(SellProductsSection, SellProductsAdmin)
