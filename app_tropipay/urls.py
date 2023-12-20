from django.urls import path

from app_tropipay.views import pay, cancel_order, fail_order, tpp_verificar, tpp_success, OrdenAPIList, OrdenAPIDetails

urlpatterns = [
    # Tropipay urls
    path('pagar/', pay, name='pagar'),
    path('tropipay/verificar/', tpp_verificar, name='tpp_verificar'),
    path('tropipay/success/', tpp_success, name='tpp_success'),
    path('tropipay/fails/', fail_order, name='orden-fail'),
    # API
    path('orden/list/', OrdenAPIList.as_view(), name='orden-api-list'),
    path('orden/<uuid>/', OrdenAPIDetails.as_view(), name='orden-api-details'),
    path('cancelar_orden/<pk>/', cancel_order, name='cancelar'),
]
