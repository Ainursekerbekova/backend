from decimal import Decimal
from django.conf import settings

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        prod_id=str(product.id)
        if prod_id not in self.cart:
            self.cart[prod_id] = {'id':product.id,'quantity': 1,'ed':str(product.edinica), 'price': product.price, 'title':product.title,'sum':product.price,'content':product.content,'img':product.img.url}
        else:
            self.cart[prod_id]['quantity'] += quantity
            summa=self.cart[prod_id]['quantity']*product.price
            self.cart[prod_id]['sum']=summa
        if update_quantity:
            self.cart[prod_id]['quantity'] = quantity
            summa=self.cart[prod_id]['quantity']*product.price
            self.cart[prod_id]['sum']=summa
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        prod_id=str(product.id)
        if prod_id in self.cart:
            del self.cart[prod_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total=0
        for item in self.cart.values():
            total+=item['price']*item['quantity']
        return total


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True