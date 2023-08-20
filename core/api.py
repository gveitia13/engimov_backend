from rest_framework import viewsets, pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView

from .models import ProductCategory, WorkCategory, Product, Work, Testimonial, EnterpriseData, JobOffer, JobOfferPool, \
    CommercialJobOffer
from .serializers import ProductCategorySerializer, WorkCategorySerializer, ProductSerializer, WorkSerializer, \
    TestimonialSerializer, EnterpriseDataSerializer, ContactSerializer, JobOfferSerializer, JobOfferPoolSerializer, \
    CommercialJobOfferSerializer
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
    queryset = ProductCategory.objects.filter(
        product__in=Product.objects.filter(visible=True, is_sale=False)).distinct().order_by('-id')
    serializer_class = ProductCategorySerializer

    # pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('index'):
            queryset = ProductCategory.objects.filter(
                product__in=Product.objects.filter(visible=True, is_sale=False)[:10]).distinct().order_by('-id')
        return queryset


class ProductInSaleCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategory.objects.filter(
        product__in=Product.objects.filter(visible=True, is_sale=True)).distinct().order_by('-id')
    serializer_class = ProductCategorySerializer


class WorkCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkCategory.objects.filter(work__in=Work.objects.all()).distinct().order_by('-id')
    serializer_class = WorkCategorySerializer
    # pagination_class = StandardResultsSetPagination


class BaseProductViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        price = self.request.query_params.get('price')
        priceup = self.request.query_params.get('priceup')
        pricedown = self.request.query_params.get('pricedown')
        category = self.request.query_params.get('category')
        order = self.request.query_params.get('order')
        if price == 'up':
            queryset = queryset.order_by('price')
        elif price == 'down':
            queryset = queryset.order_by('-price')
        if priceup:
            queryset = queryset.filter(price__gte=priceup)
        if pricedown:
            queryset = queryset.filter(price__lte=pricedown)
        if category:
            queryset = queryset.filter(category__pk=category)
        if order == 'asc':
            queryset = queryset.order_by('name')
        elif order == 'desc':
            queryset = queryset.order_by('-name')
        return queryset


class ProductViewSet(BaseProductViewSet):
    queryset = Product.objects.filter(visible=True, is_sale=False).order_by('sku')
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('index'):
            queryset = queryset[:10]
        return queryset


class ProductSaleViewSet(BaseProductViewSet):
    queryset = Product.objects.filter(visible=True, is_sale=True).order_by('sku')
    serializer_class = ProductSerializer


class WorkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Work.objects.order_by('-id')
    serializer_class = WorkSerializer
    # pagination_class = StandardResultsSetPagination


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimonial.objects.order_by('-id')
    serializer_class = TestimonialSerializer
    # pagination_class = StandardResultsSetPagination


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
        # Get all the matching products and works
        products = Product.objects.filter(name__icontains=query).order_by('pk')
        works = Work.objects.filter(name__icontains=query).order_by('pk')

        # Paginate the products
        product_paginator = SearchResultsSetPagination()
        paginated_products = product_paginator.paginate_queryset(products, request)
        serialized_products = ProductSerializer(paginated_products, many=True).data

        # Paginate the works
        work_paginator = SearchResultsSetPagination()
        paginated_works = work_paginator.paginate_queryset(works, request)
        serialized_works = WorkSerializer(paginated_works, many=True).data

        # Return the paginated results as a JSON response
        return Response({
            'products': {
                'results': serialized_products,
                'next': product_paginator.get_next_link(),
                'previous': product_paginator.get_previous_link(),
            },
            'works': {
                'results': serialized_works,
                'next': work_paginator.get_next_link(),
                'previous': work_paginator.get_previous_link(),
            },
        })


class CountView(APIView):
    def get(self, request):
        # Get the counts of products, works, product categories, and work categories
        product_count = Product.objects.count()
        work_count = Work.objects.count()
        product_category_count = ProductCategory.objects.count()
        work_category_count = WorkCategory.objects.count()

        # Return the counts as a JSON response
        return Response({
            'products': product_count,
            'works': work_count,
            'product_categories': product_category_count,
            'work_categories': work_category_count,
        })


class JobOfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if request.query_params.get('long') == 'True':
            for job_offer_data in response.data:
                job_offer = JobOffer.objects.get(pk=job_offer_data['pk'])
                job_offer_pools = job_offer.jobofferpool_set.all()
                job_offer_pools_data = JobOfferPoolSerializer(job_offer_pools, many=True).data
                job_offer_data['job_offer_pools'] = job_offer_pools_data
        return response


class JobOfferPoolViewSet(viewsets.ModelViewSet):
    queryset = JobOfferPool.objects.all()
    serializer_class = JobOfferPoolSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'create':
            return super().get_queryset()
        else:
            return JobOfferPool.objects.none()


class CommercialJobOfferViewSet(viewsets.ModelViewSet):
    queryset = CommercialJobOffer.objects.all()
    serializer_class = CommercialJobOfferSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'create':
            return super().get_queryset()
        else:
            return CommercialJobOffer.objects.none()
