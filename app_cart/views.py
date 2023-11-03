from rest_framework.decorators import api_view

from app_cart import responses
from app_cart.cart import Cart
from core.models import Product


@api_view(['POST'])
def details(request):
    if not request.headers.get('Cart-Id'):
        return responses.unauthorized()
    return responses.ok(Cart(request))


@api_view(['POST'])
def product_details(request, pk):
    if not request.headers.get('Cart-Id'):
        return responses.unauthorized()
    return responses.ok(Cart(request), pk)


@api_view(['POST'])
def add(request, pk, quantity: int):
    if not request.headers.get('Cart-Id'):
        return responses.unauthorized()

    cart = Cart(request)
    product = Product.objects.filter(pk=pk).first()
    if product:
        cart.add(product, quantity)
        return responses.ok(cart, pk)
    return responses.not_found()


@api_view(['POST'])
def update(request, pk, quantity: int):
    if not request.headers.get('Cart-Id'):
        return responses.unauthorized()

    cart = Cart(request)
    product = Product.objects.filter(pk=pk).first()
    if product:
        cart.update_quantity(product=product, quantity=quantity)
        return responses.ok(cart, pk)
    return responses.not_found()


@api_view(['POST'])
def clear(request):
    if not request.headers.get('Cart-Id'):
        return responses.unauthorized()

    cart = Cart(request)
    cart.clear()
    return responses.ok(cart)
