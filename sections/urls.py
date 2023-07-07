from django.urls import path, include
from rest_framework import routers
from .api import IndexSectionViewSet, WorkWithUsSectionViewSet, ProductsPortfolioSectionViewSet, \
    ContactUsSectionViewSet, SellProductsSectionViewSet, WorksPortfolioSectionViewSet, \
    AboutUsSectionViewSet

router = routers.DefaultRouter()
router.register('index', IndexSectionViewSet)
router.register('about', AboutUsSectionViewSet)
router.register('products_portfolio', ProductsPortfolioSectionViewSet)
router.register('works_portfolio', WorksPortfolioSectionViewSet)
router.register('work_with_us', WorkWithUsSectionViewSet)
router.register('sell', SellProductsSectionViewSet)
router.register('contact', ContactUsSectionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
