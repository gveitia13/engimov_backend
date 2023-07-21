from rest_framework import viewsets, pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from .models import ProductCategory, WorkCategory, Product, Work, Testimonial, EnterpriseData
from .serializers import ProductCategorySerializer, WorkCategorySerializer, ProductSerializer, WorkSerializer, \
    TestimonialSerializer, EnterpriseDataSerializer, ContactSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class SearchResultsSetPagination(pagination.PageNumberPagination):
    page_size = 25
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

@api_view(['POST'])
def create_contact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchPreviewView(APIView):
    def get(self, request, query):
        # Get the top 5 matching products
        products = Product.objects.filter(name__icontains=query)[:5]
        serialized_products = ProductSerializer(products, many=True).data
        # Return the results as a JSON response
        data = {
            'products': serialized_products,
        }
        return Response(data)

class SearchView(APIView):
    def get(self, request, query):
        # Get all the matching products
        products = Product.objects.filter(name__icontains=query).order_by('pk')

        # Paginate the results
        paginator = SearchResultsSetPagination()
        print(paginator.page_size)
        paginated_products = paginator.paginate_queryset(products, request)
        serialized_products = ProductSerializer(paginated_products, many=True).data

        # Return the paginated results as a JSON response
        return paginator.get_paginated_response(serialized_products)