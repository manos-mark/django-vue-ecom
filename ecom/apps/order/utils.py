import datetime
import os
from random import randint
from apps.cart.cart import Cart

from apps.order.models import Order, OrderItem

def checkout(request, first_name, last_name, email, address, zipcode, place, phone):
    """
    Params:
        -first_name:[String] Customer's first name
        -last_name:[String] Customer's last name
        -email:[String] Customer's E-mail
        -address:[String] Customer's Address
        -zipcode:[String] Customer's zipcode
        -place:[String] Customer's place
        -phone:[String] Customer's phone
    Return:
        -order.id : [String] The generated id from the order that just saved into the Database
    """
    order = Order(first_name=first_name, last_name=last_name, \
        email=email, address=address, zipcode=zipcode, place=place, phone=phone)
    # If the user is authenticated then save the already saved user's info in the order's info
    if request.user.is_authenticated:
        order.user = request.user
        
    order.save()

    cart = Cart(request)
    # Create the order 
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], \
            price=item['price'], quantity=item['quantity'])

    return order.id