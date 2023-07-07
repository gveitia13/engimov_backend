from rest_framework import viewsets
from .models import IndexSection, AboutUsSection, ProductsPortfolioSection, WorksPortfolioSection, WorkWithUsSection, \
    ContactUsSection, SellProductsSection
from .serializers import IndexSectionSerializer, AboutUsSectionSerializer, ProductsPortfolioSectionSerializer, \
    WorksPortfolioSectionSerializer, WorkWithUsSectionSerializer, ContactUsSectionSerializer, \
    SellProductsSectionSerializer


class IndexSectionViewSet(viewsets.ModelViewSet):
    queryset = IndexSection.objects.order_by('-id')
    serializer_class = IndexSectionSerializer


class AboutUsSectionViewSet(viewsets.ModelViewSet):
    queryset = AboutUsSection.objects.order_by('-id')
    serializer_class = AboutUsSectionSerializer


class ProductsPortfolioSectionViewSet(viewsets.ModelViewSet):
    queryset = ProductsPortfolioSection.objects.order_by('-id')
    serializer_class = ProductsPortfolioSectionSerializer


class WorksPortfolioSectionViewSet(viewsets.ModelViewSet):
    queryset = WorksPortfolioSection.objects.order_by('-id')
    serializer_class = WorksPortfolioSectionSerializer


class WorkWithUsSectionViewSet(viewsets.ModelViewSet):
    queryset = WorkWithUsSection.objects.order_by('-id')
    serializer_class = WorkWithUsSectionSerializer


class ContactUsSectionViewSet(viewsets.ModelViewSet):
    queryset = ContactUsSection.objects.order_by('-id')
    serializer_class = ContactUsSectionSerializer


class SellProductsSectionViewSet(viewsets.ModelViewSet):
    queryset = SellProductsSection.objects.order_by('-id')
    serializer_class = SellProductsSectionSerializer
