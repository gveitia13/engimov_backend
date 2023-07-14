from rest_framework import viewsets, pagination
from .models import ProductCategory, WorkCategory, Product, Work, Testimonial, EnterpriseData
from .serializers import ProductCategorySerializer, WorkCategorySerializer, ProductSerializer, WorkSerializer, \
    TestimonialSerializer, EnterpriseDataSerializer


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategory.objects.order_by('-id')
    serializer_class = ProductCategorySerializer
    pagination_class = StandardResultsSetPagination

class WorkCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkCategory.objects.order_by('-id')
    serializer_class = WorkCategorySerializer
    pagination_class = StandardResultsSetPagination

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(visible=True).order_by('sku')
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

class WorkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Work.objects.order_by('-id')
    serializer_class = WorkSerializer
    pagination_class = StandardResultsSetPagination

class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimonial.objects.order_by('-id')
    serializer_class = TestimonialSerializer
    pagination_class = StandardResultsSetPagination

class EnterpriseDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EnterpriseData.objects.order_by('-id')
    serializer_class = EnterpriseDataSerializer
