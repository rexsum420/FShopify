from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        price = product.sale_price if product.sale_price and product.sale_price > 0 else product.price
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(price)}
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total_price'] = float(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal_price(self):
        subtotal = sum(float(item['price']) * item['quantity'] for item in self.cart.values())
        return f"{subtotal:.2f}"

    def get_tax_price(self):
        subtotal = float(self.get_subtotal_price())
        tax = subtotal * 0.0825
        return f"{tax:.2f}"

    def get_total_price(self):
        subtotal = float(self.get_subtotal_price())
        tax = float(self.get_tax_price())
        total = subtotal + tax
        return f"{total:.2f}"

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def decrease_quantity(self, product, quantity=1):
        product_id = str(product.id)
        
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= quantity
            
            if self.cart[product_id]['quantity'] <= 0:
                del self.cart[product_id] 

            self.save()
