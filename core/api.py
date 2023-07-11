from rest_framework import viewsets, pagination
from .models import ProductCategory, WorkCategory, Product, Work, Testimonial
from .serializers import ProductCategorySerializer, WorkCategorySerializer, ProductSerializer, WorkSerializer, TestimonialSerializer



class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.order_by('-id')
    serializer_class = ProductCategorySerializer
    pagination_class = StandardResultsSetPagination

class WorkCategoryViewSet(viewsets.ModelViewSet):
    queryset = WorkCategory.objects.order_by('-id')
    serializer_class = WorkCategorySerializer
    pagination_class = StandardResultsSetPagination

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(visible=True).order_by('sku')
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.order_by('-id')
    serializer_class = WorkSerializer
    pagination_class = StandardResultsSetPagination

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.order_by('-id')
    serializer_class = TestimonialSerializer
    pagination_class = StandardResultsSetPagination