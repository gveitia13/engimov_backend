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

    def add(self, product, quantity):
        """
        Add a product to the cart its quantity.
        """
        q = int(quantity)
        stock = int(product.stock)
        prod = ProductSerializer(product).data

        if str(product.pk) not in self.cart.keys():
            prod.update({'quantity': q if q <= stock else stock})

            self.cart[str(product.pk)] = {
                "pk": str(product.pk),
                'product': prod,
            }
            print(self.cart[str(product.pk)])
        else:
            amount = int(self.cart[str(product.pk)]['product']['quantity'])
            self.cart[str(product.pk)]['product']['quantity'] = amount + q if (amount + q) <= stock else stock
            print(self.cart[str(product.pk)])
        self.save()

    def subtract(self, product, quantity=1):
        """
        Subtract a product from the cart or update its quantity.
        """
        if str(product.pk) in self.cart.keys():
            amount = int(self.get_product(product.pk)['quantity'])
            new_quantity = max(amount - int(quantity), 0)
            if new_quantity == 0:
                del self.cart[str(product.pk)]
            else:
                self.cart[str(product.pk)]['product']['quantity'] = new_quantity
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    # Devuelve el objeto en el formato que está en el carro
    def get(self, pk):
        if self.session[settings.CART_SESSION_ID].get(pk):
            return self.session[settings.CART_SESSION_ID][pk]
        return None

    def get_product(self, pk):
        if self.session[settings.CART_SESSION_ID].get(pk):
            return self.session[settings.CART_SESSION_ID][pk]['product']
        return None

    def get_all(self):
        return list(self.session[settings.CART_SESSION_ID].values())

    def get_all_products(self):
        return map(lambda e: e['product'], self.get_all())

    def set(self, key, value):
        self.cart[key] = value
        self.save()

    def get_sum_of(self, key):
        return sum(map(lambda x: float(x[key]), self.get_all_products()))

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        if str(product.pk) in self.cart.keys():
            del self.cart[str(product.pk)]
            self.save()

    def decrement(self, product, quantity):
        if str(product.pk) in self.session[settings.CART_SESSION_ID]:
            new_quantity = self.cart[str(product.pk)]['product']['quantity'] - quantity
            if new_quantity < 1:
                del self.cart[str(product.pk)]
            else:
                self.cart[str(product.pk)]['product']['quantity'] = new_quantity
        self.save()

    def update_quantity(self, product, quantity):
        q = int(quantity)
        stock = int(product.stock)
        if str(product.pk) in self.session[settings.CART_SESSION_ID]:
            if q == 0:
                self.remove(product)
                return
            if q >= stock:
                new_quantity = stock
            else:
                new_quantity = q
            self.cart[str(product.pk)]['product']['quantity'] = new_quantity
            self.save()
        else:
            self.add(product, quantity)

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total(self):
        return sum(map(lambda x: float(x['price']) * int(x['quantity']), self.get_all_products()))
