from django.contrib import admin
from .models import ProductCategory, WorkCategory, Product, Work, Testimonial

class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 0

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class WorkCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'price', 'visible')
    list_filter = ('category', 'visible')
    search_fields = ('sku', 'name')

class WorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    inlines = [TestimonialInline]

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(WorkCategory, WorkCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Work, WorkAdmin)
