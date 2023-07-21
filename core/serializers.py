from rest_framework import serializers
from .models import ProductCategory, WorkCategory, Product, Work, Testimonial, EnterpriseAditionalContact, \
    EnterpriseData, Contact


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
        fields = ('sku', 'category', 'name', 'description', 'image', 'price', 'visible')
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
        'enterprise_name', 'location', 'email', 'tel', 'address', 'enterpriseaditionalcontact_set', 'facebook',
        'twitter', 'youtube', 'instagram')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'text')
