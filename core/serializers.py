from rest_framework import serializers
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
    class Meta:
        model = Product
        fields = ('sku', 'category', 'name', 'description', 'image', 'price', 'visible', 'stock')
        depth = 1


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ('id', 'work', 'name', 'link', 'testimonial')


class WorkSerializer(serializers.ModelSerializer):
    testimonials = TestimonialSerializer(many=True, read_only=True, source='testimonial_set')

    class Meta:
        model = Work
        fields = ('id', 'category', 'name', 'description', 'image', 'testimonials')
        depth = 1


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
