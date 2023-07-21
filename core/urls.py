from django.urls import path, include
from rest_framework import routers
from .api import ProductCategoryViewSet, WorkCategoryViewSet, ProductViewSet, WorkViewSet, TestimonialViewSet, \
    EnterpriseDataViewSet, create_contact, SearchPreviewView, SearchView

router = routers.DefaultRouter()
router.register('productcategories', ProductCategoryViewSet)
router.register('workcategories', WorkCategoryViewSet)
router.register('products', ProductViewSet)
router.register('works', WorkViewSet)
router.register('testimonials', TestimonialViewSet)
router.register('enterprise_data', EnterpriseDataViewSet)

urlpatterns = [
    path('core/', include(router.urls)),
    path('core/contacts/', create_contact, name='create_contact'),
    path('search/<str:query>/preview', SearchPreviewView.as_view()),
    path('search/<str:query>', SearchView.as_view()),
]