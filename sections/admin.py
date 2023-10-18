# Register your models here.
from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import IndexSection, AboutUsSection, ProductsPortfolioSection, WorksPortfolioSection, WorkWithUsSection, \
    ContactUsSection, SellProductsSection, AboutUsSectionPerks, TermsAndPrivacyPolice


class AboutUsSectionPerksInline(admin.StackedInline):
    model = AboutUsSectionPerks
    extra = 0


class BaseSectionAdmin(SingletonModelAdmin):
    list_display = ('title', 'subtitle')
    search_fields = ('title', 'subtitle')


class AboutUsSectionAdmin(BaseSectionAdmin):
    inlines = [AboutUsSectionPerksInline, ]


admin.site.register(IndexSection, BaseSectionAdmin)
admin.site.register(AboutUsSection, AboutUsSectionAdmin)
admin.site.register(ProductsPortfolioSection, BaseSectionAdmin)
admin.site.register(WorksPortfolioSection, BaseSectionAdmin)
admin.site.register(WorkWithUsSection, BaseSectionAdmin)
admin.site.register(ContactUsSection, BaseSectionAdmin)
admin.site.register(SellProductsSection, BaseSectionAdmin)
admin.site.register(TermsAndPrivacyPolice, BaseSectionAdmin)
