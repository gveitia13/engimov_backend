import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_cart.cart import Cart
from core.models import Product
from engimovCaribe.settings import CART_SESSION_ID


@api_view(['POST'])
def details(request):
    print(request.headers)
    request.headers
    print('sesiiom   ', request.session)
    # Construct the cache key using the session ID
    cart = Cart(request)
    # Calculate the total price of the products in the shopping cart
    # total = 0
    # products = Product.objects.in_bulk(cart.session[CART_SESSION_ID].keys()).values()
    # for product in products:
    #     total += (product.price * cart.get_product(str(product.pk))['quantity'])
    # Return the shopping cart as a JSON response
    return Response({
        'products': cart.get_all_products(),
        'total': cart.get_total(),
        'total_products': len(cart.get_all())
    })


@api_view(['POST'])
def product_details(request, pk):
    cart = Cart(request)
    product = cart.get_product(pk)
    return Response({"result": product}, status=status.HTTP_200_OK)


@api_view(['POST'])
def add(request, pk, quantity: int):
    cart = Cart(request)
    product = Product.objects.filter(pk=pk).first()
    if product:
        cart.add(product, quantity)
        print(json.dumps(cart.get_all_products(), indent=4))
        return Response({
            "result": {
                'total': cart.get_total(),
                'product': cart.get_product(pk),
                'products': cart.get_all_products(),
                # "amount": cart.session[CART_SESSION_ID].get(pk)["quantity"]
            }
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update(request, pk, quantity: int):
    cart = Cart(request)
    product = Product.objects.filter(pk=pk).first()
    if product:
        cart.update_quantity(product=product, quantity=quantity)
        total = 0
        for item in cart.get_all():
            total = total + (cart.session[CART_SESSION_ID].get(item['pk'])['product']['price'] *
                             cart.session[CART_SESSION_ID].get(item['pk'])['product']['quantity'])
        return Response({
            "result": {
                'total': cart.get_total(),
                'product': cart.get_product(pk),
            }
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def decrement(request, pk, quantity: int):
    cart = Cart(request)
    product = Product.objects.filter(pk=pk).first()
    if product and cart.get(pk):
        cart.decrement(product, quantity)
        return Response({
            "result": {
                'total': cart.get_total(),
                'product': cart.get_product(pk),
            }
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def remove(request, pk):
    try:
        cart = Cart(request)
        product = Product.objects.get(pk=pk)
        cart.remove(product=product)
        return Response({
            "result": {
                'total': cart.get_total(),
                'product': cart.get_product(pk),
            }
        }, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def clear(request):
    cart = Cart(request)
    cart.clear()
    return Response({
        'result': {
            "total": cart.get_total(),
            'product': None,
        }
    }, status=status.HTTP_200_OK)
