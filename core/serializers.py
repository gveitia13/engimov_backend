from rest_framework import serializers

from engimovCaribe.utils import traducir_por_defecto
from .models import ProductCategory, WorkCategory, Product, Work, Testimonial, EnterpriseAditionalContact, \
    EnterpriseData, Contact, TermsOfUse, PrivacyPolicy, JobOffer, JobOfferPool, CommercialJobOffer


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name')


class WorkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkCategory
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    in_cart = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'sku', 'category', 'name', 'description', 'image', 'price', 'visible', 'stock', 'short_description',
            'quantity', 'in_cart')
        depth = 1

    def get_short_description(self, obj):
        return obj.description if len(obj.description) < 100 else obj.description[:100] + '...'

    def get_quantity(self, obj):
        return 1

    def get_in_cart(self, obj):
        return False


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ('id', 'work', 'name', 'testimonial')


class WorkSerializer(serializers.ModelSerializer):
    testimonials = TestimonialSerializer(many=True, read_only=True, source='testimonial_set')
    name = serializers.SerializerMethodField()

    class Meta:
        model = Work
        fields = ('id', 'category', 'name', 'description', 'image', 'testimonials')
        depth = 1

    def get_name(self, obj):
        return {
            'es': obj.name,
            'en': obj.name_en,
            'pt': obj.name_pt
        }


class EnterpriseAditionalContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnterpriseAditionalContact
        fields = ('contact_type', 'contact', 'contact_aditional_info')


class EnterpriseDataSerializer(serializers.ModelSerializer):
    enterpriseaditionalcontact_set = EnterpriseAditionalContactSerializer(many=True, read_only=True)

    class Meta:
        model = EnterpriseData
        fields = (
            'enterprise_name', 'location', 'email', 'tel', 'city', 'address', 'enterpriseaditionalcontact_set',
            'facebook', 'twitter', 'youtube', 'instagram', 'doc_folleto_digital', 'doc_presentation')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'text')


class TermsOfUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsOfUse
        fields = ('version', 'content', 'effective_date')


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ('version', 'content', 'effective_date')


class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        # fields = ('pk', 'name', 'description')
        fields = '__all__'


class JobOfferPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOfferPool
        fields = '__all__'


class CommercialJobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialJobOffer
        fields = '__all__'
