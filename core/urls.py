from django.urls import path, include
from rest_framework import routers

from .api import ProductCategoryViewSet, WorkCategoryViewSet, ProductViewSet, WorkViewSet, TestimonialViewSet, \
    EnterpriseDataViewSet, create_contact, SearchPreviewView, SearchView, CountView, ProductInSaleCategoryViewSet, \
    ProductSaleViewSet, JobOfferViewSet, JobOfferPoolViewSet, CommercialJobOfferViewSet, TermsOfUseViewSet, \
    PrivacyPolicyViewSet, DeliveryPriceViewSet, DeliveryPlaceViewSet

router = routers.DefaultRouter()
router.register('productcategories', ProductCategoryViewSet)
router.register('workcategories', WorkCategoryViewSet)
router.register('products', ProductViewSet)
router.register('products_sale', ProductSaleViewSet)
router.register('productcategories_sale', ProductInSaleCategoryViewSet)
router.register('works', WorkViewSet)
router.register('testimonials', TestimonialViewSet)
router.register('enterprise_data', EnterpriseDataViewSet)
router.register('job_offers', JobOfferViewSet)
router.register('job_offers_pool', JobOfferPoolViewSet)
router.register('commercial_job_offers', CommercialJobOfferViewSet)
router.register('terms', TermsOfUseViewSet)
router.register('privacy', PrivacyPolicyViewSet)
router.register('delivery_places', DeliveryPlaceViewSet)
router.register('delivery_prices', DeliveryPriceViewSet)

urlpatterns = [
    path('core/', include(router.urls)),
    path('core/contacts/', create_contact, name='create_contact'),
    path('search/<str:query>/preview', SearchPreviewView.as_view()),
    path('search/<str:query>', SearchView.as_view()),
    path('counts', CountView.as_view()),
]
