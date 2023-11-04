from django.core.cache import cache

from core.serializers import ProductSerializer


class Wrapper(dict):
    def __init__(self, model) -> None:
        self.__dict__ = model.__dict__
        del self.__dict__["_state"]
        super().__init__(model.__dict__)


class Cart(object):
    def __init__(self, request=None):
        if request is not None:
            self.request = request
            self.session = request.headers.get('Cart-Id')

    def add(self, product, quantity):
        """
        Add a product to the cart its quantity.
        """
        q = int(quantity)
        stock = int(product.stock)
        prod = ProductSerializer(product).data
        cart = cache.get(self.session) or {}
        if str(product.pk) not in cart:
            prod.update({'quantity': q if q <= stock else stock})
            prod.update({'in_cart': True})
            cart[str(product.pk)] = prod
        else:
            amount = int(cache.get(self.session)['quantity'])
            cart[str(product.pk)]['quantity'] = amount + q if (amount + q) <= stock else stock
        self.save(cart)

    def save(self, cart):
        cache.set(self.session, cart, 60 * 60 * 4)

    # Devuelve el objeto en el formato que está en el carro
    def get(self, pk):
        return cache.get(self.session)[str(pk)] if str(pk) in cache.get(self.session) else None

    def get_all(self):
        return list(cache.get(self.session).values()) if cache.get(self.session) else []

    def set(self, key, value):
        cache.get(self.session)[str(key)] = value

    def get_sum_of(self, key):
        return sum(map(lambda x: float(x[key]), self.get_all()))

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        cart = cache.get(self.session)
        if str(product.pk) in cart:
            del cart[str(product.pk)]
            cache.set(self.session, cart)

    def update_quantity(self, product, quantity):
        q = int(quantity)
        stock = int(product.stock)
        cart = cache.get(self.session) or {}
        print(product)
        if str(product.pk) in cart:
            if q <= 0:
                self.remove(product)
                return
            if q >= stock:
                new_quantity = stock
            else:
                new_quantity = q
            cart[str(product.pk)]['quantity'] = new_quantity
            self.save(cart)
        else:
            self.add(product, quantity)

    def clear(self):
        # empty cart
        cart = cache.get(self.session) or {}
        if cart:
            for product_id in list(cart.keys()):
                del cart[str(product_id)]
            cache.set(self.session, cart)

    def get_total(self):
        return sum(map(lambda x: float(x['price']) * int(x['quantity']), self.get_all())) if cache.get(
            self.session) else 0
