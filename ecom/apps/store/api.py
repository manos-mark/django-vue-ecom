import json
from os import setegid
import stripe

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Product

from apps.coupon.models import Coupon
from apps.cart.cart import Cart
from apps.order.utils import checkout
from apps.order.models import Order

def api_create_checkout_session(request):
    data = json.loads(request.body)

    # Coupon
    coupon_code = data['coupon_code']
    coupon_value = 0

    if coupon_code != '':
        coupon = Coupon.objects.get(code=coupon_code)
        
        if coupon.can_use():
            coupon_value = coupon.value
            coupon.use()
    #

    cart = Cart(request)
    items = []

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    
    for item in cart:
        product = item['product']
        price = int(product.price * 100)

        if coupon_value > 0:
            price = int( price * (int(coupon_value)/100) )

        obj = {
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': product.title
                },
                'unit_amount': price
            },
            'quantity': item['quantity']
        }
        items.append(obj)

    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = items,
        mode = 'payment',
        success_url = 'http://127.0.0.1:8000/cart/success/',
        cancel_url = 'http://127.0.0.1:8000/cart/',
    )

    #
    # Create order
    #
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zipcode']
    place = data['place']
    phone = data['phone']

    orderid = checkout(request, first_name, last_name, email, address, zipcode, place, phone)

    total_price = 0.0
    for item in cart:
        product = item['product']
        total_price += (float(product.price) * int(item['quantity']))

    if coupon_value > 0:
        total_price = total_price * (coupon_value/100)

    order = Order.objects.get(pk=orderid)
    order.payment_intent = session.payment_intent
    
    order.paid_amount = total_price
    order.used_coupon = coupon_code
    order.save()

    return JsonResponse({'session': session})

def api_add_to_cart(request):
    data = json.loads(request.body)

    jsonresponse = {'success': True}
    product_id = data['product_id']
    update = data['update_quantity']
    quantity = data['quantity']

    cart = Cart(request)

    product = get_object_or_404(Product, pk=product_id)

    if not update:
        cart.add(product=product, quantity=1, update_quantity=False)
    else:
        cart.add(product=product, quantity=quantity, update_quantity=True)

    return JsonResponse(jsonresponse)

def api_remove_from_cart(request):
    data = json.loads(request.body)

    jsonresponse = {'success': True}
    product_id = str(data['product_id'])

    cart = Cart(request)
    cart.remove(product_id)

    return JsonResponse(jsonresponse)
