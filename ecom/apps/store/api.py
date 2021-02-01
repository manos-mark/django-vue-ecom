import json
from os import setegid
import stripe

from django.http import HttpResponseBadRequest
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Product, Store, StoreAdmin

from apps.store import utils
from apps.userprofile.models import Userprofile
from apps.coupon.models import Coupon
from apps.cart.cart import Cart
from apps.order.utils import checkout
from apps.order.models import Order
from apps.store.models import Category

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
        return HttpResponseBadRequest('Product is not available in stock!')

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

from django import forms

@csrf_exempt
@login_required
def api_create_store(request):

    store = None
    try:
        store = Store.objects.get(name=request.POST.get('name'))
    except:
        print("Store " + request.POST.get('name') + " doesn't exists. Creating one...")
    finally:
        if store:
            return HttpResponseBadRequest('Store already exists, with this name!')

    store = Store(
        name = request.POST.get('name'),
        email = request.POST.get('email'),
        address = request.POST.get('address'),
        zipcode = request.POST.get('zipcode'),
        phone = request.POST.get('phone'),
        image = request.FILES.get('image')
    )
    
    user = get_object_or_404(User, id=request.user.id)
    store_admin = StoreAdmin(store=store, user=user)

    store.save()
    store_admin.save()

    return redirect('frontpage')

@csrf_exempt
@login_required
def api_create_product(request):
    if request.method == 'POST' and request.user.is_authenticated:

        try:
            category_id = request.POST.get('category')
            category = get_object_or_404(Category, id=category_id)
            owned_stores = utils.get_owned_stores(request)

            if category.store in owned_stores:
                title = request.POST.get('title')
                description = request.POST.get('description')
                price = float(request.POST.get('price'))
                is_featured = False if request.POST.get('is_featured') == 'false' else True
                image = request.FILES.get('image')
                num_available = int(request.POST.get('num_available'))
                store = category.store
                
                product = Product(store=store, title=title, is_featured=is_featured, category=category, description=description, price=price, num_available=num_available, image=image)

                product.thumbnail = product.make_thumbnail(product.image)

                product.save()
                return redirect('product_detail', category_slug=category.slug, slug=product.slug)

        except Exception as e:
            return HttpResponseBadRequest(e)

@csrf_exempt
@login_required
def api_edit_product(request):
    if request.method == 'POST' and request.user.is_authenticated:

        product = get_object_or_404(Product, id=request.POST.get('id'))

        try:
            category_id = request.POST.get('category')
            product.category = get_object_or_404(Category, id=category_id)
            owned_stores = utils.get_owned_stores(request)

            if product.category.store in owned_stores:
                product.title = request.POST.get('title')
                product.description = request.POST.get('description')
                product.price = float(request.POST.get('price'))
                product.is_featured = False if request.POST.get('is_featured') == 'false' else True
                product.num_available = int(request.POST.get('num_available'))
                
                if request.FILES.get('image'):
                    product.image = request.FILES.get('image')
                    product.thumbnail = product.make_thumbnail(product.image)

                product.save()
                return redirect('product_detail', category_slug=product.category.slug, slug=product.slug)

        except Exception as e:
            return HttpResponseBadRequest(e)

@csrf_exempt
@login_required
def api_create_category(request):
    if request.method == 'POST' and request.user.is_authenticated:

        try:
            store_id = int(request.POST.get('store_id'))
            store = get_object_or_404(Store, id=store_id)
            owned_stores = utils.get_owned_stores(request)

            if store in owned_stores:
                title = request.POST.get('title')
                parent_id = request.POST.get('parent')
                parent = get_object_or_404(Category, id=parent_id)
                ordering = int(request.POST.get('ordering'))
                is_featured = False if request.POST.get('is_featured') == 'false' else True
                image = request.FILES.get('image')
                
                category = Category(parent=parent, store=store, title=title, is_featured=is_featured, ordering=ordering, image=image)

                category.save()
                return redirect('category_detail', slug=category.slug)

        except Exception as e:
            return HttpResponseBadRequest(e)

@csrf_exempt
@login_required
def api_edit_category(request):
    if request.method == 'POST' and request.user.is_authenticated:

        category = get_object_or_404(Category, id=request.POST.get('id'))

        try:
            owned_stores = utils.get_owned_stores(request)
            if category.store in owned_stores:
                parent_id = int(request.POST.get('parent'))
                category.parent = get_object_or_404(Category, id=parent_id)
                category.title = request.POST.get('title')
                category.ordering = int(request.POST.get('ordering'))
                category.is_featured = False if request.POST.get('is_featured') == 'false' else True
                
                if request.FILES.get('image'):
                    category.image = request.FILES.get('image')

                category.save()
                return redirect('category_detail', slug=category.slug)

        except Exception as e:
            return HttpResponseBadRequest(e)

@csrf_exempt
@login_required
def api_delete_category(request):
    if request.method == 'DELETE' and request.user.is_authenticated:

        try:
            data = json.loads(request.body)

            category_id = data['category_id']
            category = get_object_or_404(Category, id=category_id)

            store = get_object_or_404(Store, id=category.store.id)
            owned_stores = utils.get_owned_stores(request)

            if store in owned_stores:
                category.delete()
                return redirect('store_detail', slug=category.store.slug)

        except Exception as e:
            return HttpResponseBadRequest(e)

@csrf_exempt
@login_required
def api_delete_product(request):
    if request.method == 'DELETE' and request.user.is_authenticated:

        try:
            data = json.loads(request.body)

            product_id = data['product_id']
            product = get_object_or_404(Product, id=product_id)

            store = get_object_or_404(Store, id=product.store.id)
            owned_stores = utils.get_owned_stores(request)

            if store in owned_stores:
                product.delete()
                return redirect('category_detail', slug=product.category.slug)

        except Exception as e:
            return HttpResponseBadRequest(e)