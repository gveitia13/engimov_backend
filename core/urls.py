from django.urls import path, include
from rest_framework import routers
from .api import ObtainJWTView, ProductCategoryViewSet, WorkCategoryViewSet, ProductViewSet, WorkViewSet, TestimonialViewSet

router = routers.DefaultRouter()
router.register('productcategories', ProductCategoryViewSet)
router.register('workcategories', WorkCategoryViewSet)
router.register('products', ProductViewSet)
router.register('works', WorkViewSet)
router.register('testimonials', TestimonialViewSet)

urlpatterns = [
    path('api/auth/', ObtainJWTView.as_view()),
    path('api/', include(router.urls)),
]