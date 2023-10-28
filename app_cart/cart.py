from core.serializers import ProductSerializer
from engimovCaribe import settings


class Wrapper(dict):
    def __init__(self, model) -> None:
        self.__dict__ = model.__dict__
        del self.__dict__["_state"]
        super().__init__(model.__dict__)


class Cart(object):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:  # or True:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        """
        Add a product to the cart its quantity.
        """
        q = int(quantity)
        stock = int(product.stock)
        if str(product.pk) not in self.cart.keys():
            self.cart[str(product.pk)] = {
                "pk": str(product.pk),
                'product': ProductSerializer(product).data,
                'quantity': q if q <= stock else stock
            }
            print(self.cart[str(product.pk)])
        else:
            amount = int(self.cart[str(product.pk)]['quantity'])
            self.cart[str(product.pk)]['quantity'] = amount + q if (amount + q) <= stock else stock
            print(self.cart[str(product.pk)])
        self.save()

    def subtract(self, product, quantity=1):
        """
        Subtract a product from the cart or update its quantity.
        """
        q = int(quantity)
        if str(product.pk) in self.cart.keys():
            amount = int(self.cart[str(product.pk)]['quantity'])
            new_quantity = max(amount - q, 0)
            if new_quantity == 0:
                del self.cart[str(product.pk)]
            else:
                self.cart[str(product.pk)]['quantity'] = new_quantity
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def get(self, pk):
        if self.session[settings.CART_SESSION_ID][pk]:
            return self.session[settings.CART_SESSION_ID][pk]
        return None

    def all(self):
        return list(self.session[settings.CART_SESSION_ID].values())

    def set(self, key, value):
        self.cart[key] = value
        self.save()

    def get_sum_of(self, key):
        return sum(map(lambda x: float(x[key]), self.all()))

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        if str(product.pk) in self.cart:
            del self.cart[str(product.pk)]
            self.save()

    def pop(self):
        if len(self.all()) > 0:
            del self.session[settings.CART_SESSION_ID][str(self.all().pop()['pk'])]
            self.save()

    def decrement(self, product):
        if str(product.pk) in self.session[settings.CART_SESSION_ID]:
            new_quantity = self.cart[str(product.pk)]['quantity'] - 1
            if new_quantity < 1:
                del self.cart[str(product.pk)]
            else:
                self.cart[str(product.pk)]['quantity'] = new_quantity
        self.save()

    # mio
    def update_quant(self, product, value):
        q = int(value)
        stock = int(product.stock)
        if str(product.pk) in self.session[settings.CART_SESSION_ID]:
            if q >= stock:
                new_quantity = stock
            else:
                new_quantity = q
            self.cart[str(product.id)]['quantity'] = new_quantity

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
