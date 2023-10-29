from django.core.cache import cache
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from app_cart.cart import Cart
from core.models import Product
from core.serializers import ProductSerializer
from engimovCaribe.settings import CART_SESSION_ID


class CartView(APIView):
    def get(self, request):
        # Construct the cache key using the session ID
        cart = Cart(request)
        # Calculate the total price of the products in the shopping cart
        total = 0
        products = Product.objects.in_bulk(cart.session[CART_SESSION_ID].keys()).values()
        for product in products:
            total += (product.price * cart.get(str(product.pk))['quantity'])
        # Return the shopping cart as a JSON response
        return Response({
            'products': cart.all(),
            'total': total,
            'cantReal': len(cart.all())
        })


@api_view(['POST'])
def add(request: HttpRequest, pk):
    cart = Cart(request)
    product = Product.objects.filter(pk=pk).first()
    if product:
        cart.add(product=product)
        return Response({
            'result': {
                'product': ProductSerializer(product).data,
                "amount": cart.session[CART_SESSION_ID].get(pk)["quantity"]
            }
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def cart_detail(request: HttpRequest, pk):
    cart = Cart(request)
    item = cart.get(pk)
    return Response({"result": item}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_quant(request: HttpRequest, pk, quantity: int):
    cart = Cart(request)
    product = Product.objects.filter(pk=pk).first()
    if product:
        cart.update_quant(product=product, quantity=quantity)
        total = 0
        for item in cart.all():
            total = total + (cart.session[CART_SESSION_ID].get(item)['product']['price'] *
                             cart.session[CART_SESSION_ID].get(item)['quantity'])
        return Response({
            "result": {
                "total": total,
                'product': ProductSerializer(product).data,
                "amount": cart.session[CART_SESSION_ID].get(pk)["quantity"],
            }
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def decrement(request: HttpRequest, pk):
    product = Product.objects.filter(pk=pk).first()
    if product:
        Cart(request).decrement(product=product)
        return Response({"result": "ok"}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def cart_pop(request: HttpRequest, ):
    cart = Cart(request)
    cart.pop()
    return Response({"result": {"amount": cart.get_sum_of("quantity")}}, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_quant(request: HttpRequest, pk, quantity: int):
    cart = Cart(request)
    product = Product.objects.filter(pk=pk).first()
    if product:
        cart.add(product, quantity)
        return Response({
            "result": {
                'product': ProductSerializer(product).data,
                "amount": cart.session[CART_SESSION_ID].get(pk)["quantity"]
            }
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def decrement_quant(request: HttpRequest, pk, quantity: int):
    cart = Cart(request)
    product = Product.objects.filter(pk=pk).first()
    if product:
        cart.subtract(product, quantity)
        return Response({
            'result': {
                'product': ProductSerializer(product).data,
                "amount": cart.session[CART_SESSION_ID].get(pk)["quantity"]
            }
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def remove(request: HttpRequest, pk):
    try:
        cart = Cart(request)
        product = Product.objects.get(pk=pk)
        cart.remove(product=product)
        return Response({
            'result': {
                'product': ProductSerializer(product).data,
                "amount": cart.get_sum_of("quantity")
            }
        }, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def cart_clear(request: HttpRequest):
    Cart(request).clear()
    return Response({
        'result': {
            'product': None,
            "amount": 0
        }}, status=status.HTTP_200_OK)
