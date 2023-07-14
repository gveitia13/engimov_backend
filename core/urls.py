from django.urls import path, include
from rest_framework import routers
from .api import ProductCategoryViewSet, WorkCategoryViewSet, ProductViewSet, WorkViewSet, TestimonialViewSet, \
    EnterpriseDataViewSet

router = routers.DefaultRouter()
router.register('productcategories', ProductCategoryViewSet)
router.register('workcategories', WorkCategoryViewSet)
router.register('products', ProductViewSet)
router.register('works', WorkViewSet)
router.register('testimonials', TestimonialViewSet)
router.register('enterprise_data', EnterpriseDataViewSet)

urlpatterns = [
    path('core/', include(router.urls)),
]