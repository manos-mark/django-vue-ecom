from django.conf import settings
from django.shortcuts import render

from .cart import Cart

def cart_detail(request):
    """
    Renders the cart page, getting a list of ordered products to render them 
    Return:
        -[Render] Renders the cart.html
    """
    cart = Cart(request)
    productsstring = ''

    for item in cart:
        product = item['product']
        url = '/%s/%s/' % (product.category.slug, product.slug)
        b = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s', \
            'total_price': '%s', 'thumbnail': '%s', 'url': '%s', 'num_available': '%s'}," \
            %(product.id, product.title, product.price, item['quantity'], \
            item['total_price'], product.thumbnail.url, url, product.num_available)
        productsstring += b
    # Checks if the request is authenticated to get whole information about the user
    # and render them in the contact information form
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        address = request.user.userprofile.address
        zipcode = request.user.userprofile.zipcode
        place = request.user.userprofile.place
        phone = request.user.userprofile.phone
    else:
    # If it is not authentiated set empty strings
        first_name = last_name = email = address = zipcode = place = phone = ''

    context = {
        'cart': cart,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'address': address,
        'zipcode': zipcode,
        'place': place,
        'pub_key': settings.STRIPE_API_KEY_PUBLISHABLE,
        'productsstring': productsstring,
    }
    return render(request, 'cart.html', context)

def success(request):
    """
    Cleans the cart if the order has finished
    Return:
        -[Render] Renders the success.html
    """
    cart = Cart(request)
    cart.clear()
    return render(request, 'success.html')