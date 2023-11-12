from rest_framework import serializers
from .models import IndexSection, AboutUsSection, ProductsPortfolioSection, WorksPortfolioSection, WorkWithUsSection, \
    ContactUsSection, SellProductsSection, TermsAndPrivacyPolice


class BaseSectionsSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    subtitle = serializers.SerializerMethodField()

    def get_title(self, obj):
        return {
            'es': obj.title,
            'en': obj.title_en,
            'pt': obj.title_pt
        }

    def get_subtitle(self, obj):
        return {
            'es': obj.subtitle,
            'en': obj.subtitle_en,
            'pt': obj.subtitle_pt
        }


class IndexSectionSerializer(BaseSectionsSerializer):
    class Meta:
        model = IndexSection
        fields = ('title', 'subtitle', 'image')


class AboutUsSectionSerializer(BaseSectionsSerializer):
    class Meta:
        model = AboutUsSection
        fields = ('title', 'subtitle', 'image', 'aboutussectionperks_set')
        depth = 1


class ProductsPortfolioSectionSerializer(BaseSectionsSerializer):
    class Meta:
        model = ProductsPortfolioSection
        fields = ('title', 'subtitle', 'image')


class WorksPortfolioSectionSerializer(BaseSectionsSerializer):
    class Meta:
        model = WorksPortfolioSection
        fields = ('title', 'subtitle', 'image')


class WorkWithUsSectionSerializer(BaseSectionsSerializer):
    class Meta:
        model = WorkWithUsSection
        fields = ('title', 'subtitle', 'image')


class ContactUsSectionSerializer(BaseSectionsSerializer):
    class Meta:
        model = ContactUsSection
        fields = ('title', 'subtitle', 'image')


class SellProductsSectionSerializer(BaseSectionsSerializer):
    class Meta:
        model = SellProductsSection
        fields = ('title', 'subtitle', 'image')


class TermsAndPrivacyPoliceSerializer(BaseSectionsSerializer):
    class Meta:
        model = TermsAndPrivacyPolice
        fields = ('title', 'subtitle', 'image')
