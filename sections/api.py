from rest_framework import viewsets
from .models import IndexSection, AboutUsSection, ProductsPortfolioSection, WorksPortfolioSection, WorkWithUsSection, \
    ContactUsSection, SellProductsSection
from .serializers import IndexSectionSerializer, AboutUsSectionSerializer, ProductsPortfolioSectionSerializer, \
    WorksPortfolioSectionSerializer, WorkWithUsSectionSerializer, ContactUsSectionSerializer, \
    SellProductsSectionSerializer


class IndexSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndexSection.objects.order_by('-id')
    serializer_class = IndexSectionSerializer


class AboutUsSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AboutUsSection.objects.order_by('-id')
    serializer_class = AboutUsSectionSerializer


class ProductsPortfolioSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductsPortfolioSection.objects.order_by('-id')
    serializer_class = ProductsPortfolioSectionSerializer


class WorksPortfolioSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorksPortfolioSection.objects.order_by('-id')
    serializer_class = WorksPortfolioSectionSerializer


class WorkWithUsSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkWithUsSection.objects.order_by('-id')
    serializer_class = WorkWithUsSectionSerializer


class ContactUsSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContactUsSection.objects.order_by('-id')
    serializer_class = ContactUsSectionSerializer


class SellProductsSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SellProductsSection.objects.order_by('-id')
    serializer_class = SellProductsSectionSerializer
