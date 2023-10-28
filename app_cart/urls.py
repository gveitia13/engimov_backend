from django.urls import path

from app_cart.views import *

urlpatterns = [
    path("cart/add/<pk>/", add, name="cart_add"),
    path("cart/add/<pk>/<int:quantity>/", add_quant, name="cart_add_quantity"),
    path("cart/decrement/<pk>/<int:quantity>/", decrement_quant, name="cart_decrement_quantity"),
    path("cart/remove/<pk>/", remove, name="cart_remove"),
    # actualizar cantidad
    path('cart/update_quantity/<pk>/<value>/', update_quant, name='cart_update_quantity'),
    path("cart/remove/<pk>/<quantity>/", remove_quant, name="cart_remove_quantity"),
    path("cart/clear/", cart_clear, name="cart_clear"),
    path("cart/pop/", cart_pop, name="cart_pop"),
    path("cart/clear/<pk>/", item_clear, name="cart_clear_id"),
    path("cart/details/<pk>/", cart_detail, name="cart_detail"),
    path('cart/<str:session_id>/', CartView.as_view()),
]
