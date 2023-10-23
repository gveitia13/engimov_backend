from django.core.cache import cache
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from app_cart.cart import Cart
from core.models import Product
from core.serializers import ProductSerializer
from engimovCaribe.settings import CART_SESSION_ID


@method_decorator(csrf_exempt, require_POST)
def add(request: HttpRequest, id):
    cart = Cart(request)
    product = Product.objects.filter(pk=id).first()
    cart.add(product=product)
    return JsonResponse({
        'product': ProductSerializer(product).data,
        "result": "ok",
        "amount": cache.get(cart.session)[str(product.pk)]
    })


@method_decorator(csrf_exempt, require_POST)
def cart_detail(request: HttpRequest, id):
    cart = Cart(request)
    item = cart.get(id)

    return JsonResponse({"result": item})


@method_decorator(csrf_exempt, require_POST)
def remove_quant(request: HttpRequest, id, quantity: int):
    Cart(request).add(product=Product.objects.filter(pk=id).first(), quantity=quantity, action="remove")
    return JsonResponse({"result": "ok"})


@method_decorator(csrf_exempt, require_POST)
def update_quant(request: HttpRequest, id, value: int):
    cart = Cart(request)
    product = Product.objects.get(pk=id)
    cart.update_quant(product=product, value=value)
    return JsonResponse({
        "result": "ok",
        'product': ProductSerializer(product).data,
        "amount": cart.session[CART_SESSION_ID].get(id, {"quantity": value})["quantity"],
        'price': f'{product.price}'
    })


@method_decorator(csrf_exempt, require_POST)
def update_quant_bl(request: HttpRequest, id, value: int):
    cart = Cart(request)
    product = Product.objects.get(pk=id)
    cart.update_quant(product=product, value=value)
    total = 0
    for item in cart.session[CART_SESSION_ID]:
        total = total + (cart.session[CART_SESSION_ID].get(item)['product']['price'] *
                         cart.session[CART_SESSION_ID].get(item)['quantity'])
    return JsonResponse({
        "result": "ok",
        "total": total,
        'product': ProductSerializer(product).data,
        "amount": cart.session[CART_SESSION_ID].get(id, {"quantity": value})["quantity"],
        'price': f'{product.price}'
    })


@method_decorator(csrf_exempt, require_POST)
def remove(request: HttpRequest, id):
    Cart(request).decrement(product=Product.objects.filter(pk=id).first())
    request.session['active'] = '2'
    return JsonResponse({"result": "ok"})


@method_decorator(csrf_exempt, require_POST)
def cart_pop(request: HttpRequest, ):
    cart = Cart(request)
    cart.pop()
    request.session['active'] = '2'
    return JsonResponse({
        "result": "ok",
        "amount": cart.get_sum_of("quantity")
    })


@method_decorator(csrf_exempt, require_POST)
def add_quant(request: HttpRequest, id, quantity: int):
    cart = Cart(request)
    product = Product.objects.get(pk=id)
    cart.add(product, quantity)
    return JsonResponse({
        'product': ProductSerializer(product).data,
        "result": "ok",
        "amount": cache.get(cart.session)[str(product.pk)]
    })


@method_decorator(csrf_exempt, require_POST)
def decrement_quant(request: HttpRequest, id, quantity: int):
    cart = Cart(request)
    product = Product.objects.get(pk=id)
    cart.subtract(product, quantity)
    return JsonResponse({
        'product': ProductSerializer(product).data,
        "result": "ok",
        "amount": cache.get(cart.session)[str(product.pk)]
    })


@method_decorator(csrf_exempt, require_POST)
def item_clear(request: HttpRequest, id):
    try:
        cart = Cart(request)
        product = Product.objects.get(pk=id)
        cart.remove(product=product)
        return JsonResponse({
            'product': ProductSerializer(product).data,
            "result": "ok",
            "amount": cart.get_sum_of("quantity")
        })
    except:
        return JsonResponse({
            "status": 403,
            "result": "ko",
        })


@method_decorator(csrf_exempt, require_POST)
def cart_clear(request: HttpRequest):
    Cart(request).clear()
    return JsonResponse({
        'product': None,
        "result": "ok",
        "amount": 0
    })
