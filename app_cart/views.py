import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_cart.cart import Cart
from core.models import Product


@api_view(['POST'])
def details(request):
    if not request.headers.get('Cart-Id'):
        return Response({'error': 'Debe añadir el Cart-Id a los headers del request.'},
                        status=status.HTTP_401_UNAUTHORIZED)
    cart = Cart(request)
    return Response({
        'product_list': cart.get_all(),
        'total': cart.get_total(),
        'total_products': len(cart.get_all())
    })


@api_view(['POST'])
def product_details(request, pk):
    if not request.headers.get('Cart-Id'):
        return Response({'error': 'Debe añadir el Cart-Id a los headers del request.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    cart = Cart(request)
    product = cart.get(pk)
    return Response({"result": product}, status=status.HTTP_200_OK)


@api_view(['POST'])
def add(request, pk, quantity: int):
    if not request.headers.get('Cart-Id'):
        return Response({'error': 'Debe añadir el Cart-Id a los headers del request.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    cart = Cart(request)
    product = Product.objects.filter(pk=pk).first()
    if product:
        cart.add(product, quantity)
        print(json.dumps(cart.get_all(), indent=4))
        return Response({
            "result": {
                'total': cart.get_total(),
                'product': cart.get(pk),
                'product_list': cart.get_all(),
            }
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update(request, pk, quantity: int):
    if not request.headers.get('Cart-Id'):
        return Response({'error': 'Debe añadir el Cart-Id a los headers del request.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    cart = Cart(request)
    product = Product.objects.filter(pk=pk).first()
    if product:
        cart.update_quantity(product=product, quantity=quantity)
        return Response({
            "result": {
                'total': cart.get_total(),
                'product': cart.get(pk),
                'product_list': cart.get_all(),
            }
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def clear(request):
    if not request.headers.get('Cart-Id'):
        return Response({'error': 'Debe añadir el Cart-Id a los headers del request.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    cart = Cart(request)
    cart.clear()
    return Response({
        'result': {
            "total": cart.get_total(),
            'product': None,
        }
    }, status=status.HTTP_200_OK)
