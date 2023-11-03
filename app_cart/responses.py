from rest_framework import status
from rest_framework.response import Response

from app_cart.cart import Cart


def ok(cart: Cart, pk=0):
    return Response({
        "result": {
            'total': cart.get_total(),
            'product': cart.get(pk),
            'product_list': cart.get_all(),
        }
    }, status=status.HTTP_200_OK)


def not_found():
    return Response(status=status.HTTP_404_NOT_FOUND)


def unauthorized(error_message='Debe añadir el Cart-Id a los headers del request.'):
    return Response({'error': error_message},
                    status=status.HTTP_401_UNAUTHORIZED)
