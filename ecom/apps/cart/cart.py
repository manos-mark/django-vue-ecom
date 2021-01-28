from django.conf import settings

from apps.store.models import Product

class Cart(object):
    """
    The cart as an object
    """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()

        product_clean_ids = []

        for p in product_ids:
            product_clean_ids.append(p)
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
        
        for item in self.cart.values():
            item['total_price'] = float(item['price']) * int(item['quantity'])
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product):
        """
        Update the cart if the user add a product
        Params:
            -product:[Models.Object] The product that the user have selected
        """
        product_id = str(product.id)
        price = product.price
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': price, 'id': product_id}

        self.cart[product_id]['quantity'] += 1

        self.save()

    def has_product(self, product_id):
        """
        Checks if the card have products
        Return:
            -[Boolean] True if the cart is not empty, False if the cart is empty
        """
        if str(product_id) in self.cart:
            return True
        else:
            return False

    def remove(self, product_id, quantity):
        """
        Decrements the quantity of the products according to quantity parameter
        Params:
            -product_id:[String] The product that the user would like to remove
            -quantity:[Integer] The quantity of this specific product that they want to remove
        """
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= quantity

            if self.cart[product_id]['quantity'] == 0:
                del self.cart[product_id]
            self.save()

    def save(self):
        """
        Saves the carts session
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        """
        Clears the cart session
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
        
    def get_total_length(self):
        """
        Returns the total ammount of ordered products
        Return:
            -[Integer] The sum of the products that the customers have ordered
        """
        return sum(int(item['quantity']) for item in self.cart.values())

    def get_total_cost(self):
        """
        Receives the total cost of the product contained in the cart
        Return:
            -[Integer] The sum of the product's prices
        """
        return sum(float(item['total_price']) for item in self)