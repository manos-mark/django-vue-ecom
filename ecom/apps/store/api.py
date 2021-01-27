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
    orderid = checkout(request, data['first_name'], data['last_name'], data['email'], \
        data['address'], data['zipcode'], data['place'], data['phone'])

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

    cart = Cart(request)

    product = get_object_or_404(Product, pk=product_id)

    if (product.num_available <= 0):
        return JsonResponse({'status': 400, 'message': 'Product is not available in stock!'})

    cart.add(product=product)

    product.num_available -= 1
    product.save()

    return JsonResponse(jsonresponse)

def api_remove_from_cart(request):
    data = json.loads(request.body)

    jsonresponse = {'success': True}

    product_id = str(data['product_id'])
    quantity = int(data['quantity'])

    cart = Cart(request)
    cart.remove(product_id, quantity)

    product = get_object_or_404(Product, pk=product_id)
    product.num_available += quantity
    product.save()

    return JsonResponse(jsonresponse)
