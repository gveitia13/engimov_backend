from django.urls import path, include
from rest_framework import routers
from .api import IndexSectionViewSet, WorkWithUsSectionViewSet, ProductsPortfolioSectionViewSet, \
    ContactUsSectionViewSet, SellProductsSectionViewSet, WorksPortfolioSectionViewSet, \
    AboutUsSectionViewSet, TermsAndPrivacyPoliceViewSet

router = routers.DefaultRouter()
router.register('index', IndexSectionViewSet)
router.register('about', AboutUsSectionViewSet)
router.register('products_portfolio', ProductsPortfolioSectionViewSet)
router.register('works_portfolio', WorksPortfolioSectionViewSet)
router.register('work_with_us', WorkWithUsSectionViewSet)
router.register('sell', SellProductsSectionViewSet)
router.register('contact', ContactUsSectionViewSet)
router.register('terms_privacy-police', TermsAndPrivacyPoliceViewSet)

urlpatterns = [
    path('sections/', include(router.urls)),
]
