from django.urls import path

from app_cart.views import *

urlpatterns = [
    # Añade un producto con cantidad 1 o suma la cantidad (máximo hasta el stock)
    path("add/<pk>/", add, name="cart_add"),
    # Añade un producto con cantidad determinada o suma la cantidad (máximo hasta el stock)
    path("add/<pk>/<int:quantity>/", add_quantity, name="cart_add_quantity"),
    # Decrementa en uno la cantidad del producto o elimina el producto si llega a 0
    path("decrement/<pk>/", decrement, name="cart_decrement"),
    # Decrementa la cantidad de un producto o elimina el producto si llega a 0
    path("decrement/<pk>/<int:quantity>/", decrement_quantity, name="cart_decrement_quantity"),
    # Sobreescribe la cantidad del producto en el carrito, si se pasa del stock coge el stock de cantidad
    path('update_quantity/<pk>/<int:quantity>/', update_quantity, name='cart_update_quantity'),
    # Vacía el carrito
    path("clear/", cart_clear, name="cart_clear"),
    # Elimina un producto específico del carrito
    path("remove/<pk>/", remove, name="cart_remove"),
    # Detalles de un producto específico en el carrito o None
    path("details/<pk>/", product_details, name="cart_product_details"),
    # Detalles de todos los productos del carrito
    path('details/', details, name='cart_details'),
]
