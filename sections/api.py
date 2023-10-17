import datetime

from rest_framework import viewsets

from core.models import TermsOfUse, PrivacyPolicy
from .models import IndexSection, AboutUsSection, ProductsPortfolioSection, WorksPortfolioSection, WorkWithUsSection, \
    ContactUsSection, SellProductsSection, TermsAndPrivacyPolice
from .serializers import IndexSectionSerializer, AboutUsSectionSerializer, ProductsPortfolioSectionSerializer, \
    WorksPortfolioSectionSerializer, WorkWithUsSectionSerializer, ContactUsSectionSerializer, \
    SellProductsSectionSerializer, TermsAndPrivacyPoliceSerializer


class IndexSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndexSection.objects.order_by('-id')
    serializer_class = IndexSectionSerializer


class AboutUsSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AboutUsSection.objects.order_by('-id')
    serializer_class = AboutUsSectionSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        extension = request.query_params.get('extension')
        if extension == 'long':
            try:
                terms_of_use = TermsOfUse.objects.all()[0]
            except IndexError:
                terms_of_use = TermsOfUse(version=1, content="Placeholder content",
                                          effective_date=datetime.datetime.now())
                terms_of_use.save()
            try:
                privacy_policy = PrivacyPolicy.objects.all()[0]
            except IndexError:
                privacy_policy = PrivacyPolicy(version=1, content="Placeholder content",
                                               effective_date=datetime.datetime.now())
                privacy_policy.save()
            additional_data = {
                'terms_of_use': {
                    'version': terms_of_use.version,
                    'content': terms_of_use.content,
                    'effective_date': terms_of_use.effective_date
                },
                'privacy_policy': {
                    'version': privacy_policy.version,
                    'content': privacy_policy.content,
                    'effective_date': privacy_policy.effective_date
                }
            }
            response.data.append(additional_data)
        return response


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


class TermsAndPrivacyPoliceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TermsAndPrivacyPolice.objects.order_by('-id')
    serializer_class = TermsAndPrivacyPoliceSerializer
