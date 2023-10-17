from rest_framework import serializers
from .models import IndexSection, AboutUsSection, ProductsPortfolioSection, WorksPortfolioSection, WorkWithUsSection, \
    ContactUsSection, SellProductsSection, TermsAndPrivacyPolice


class IndexSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexSection
        fields = ('title', 'subtitle', 'image')


class AboutUsSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsSection
        fields = ('title', 'subtitle', 'image', 'aboutussectionperks_set')
        depth = 1


class ProductsPortfolioSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsPortfolioSection
        fields = ('title', 'subtitle', 'image')


class WorksPortfolioSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorksPortfolioSection
        fields = ('title', 'subtitle', 'image')


class WorkWithUsSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkWithUsSection
        fields = ('title', 'subtitle', 'image')


class ContactUsSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsSection
        fields = ('title', 'subtitle', 'image')


class SellProductsSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellProductsSection
        fields = ('title', 'subtitle', 'image')


class TermsAndPrivacyPoliceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndPrivacyPolice
        fields = ('title', 'subtitle', 'image')
