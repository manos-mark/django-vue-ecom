import random
from datetime import datetime

from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Product, Category, ProductReview, Store
from apps.store import utils

from apps.cart.cart import Cart

from .forms import AddCategoryForm, EditCategoryForm, AddProductForm, EditProductForm

def search(request):
    """
    A search ability to find products by providing a string.
    The user's provided string is filtered in the database. 
    The search is triggered in title and the description
    Return:
        -[Render] Renders the search.html containing the results
    """
    query = request.GET.get('query')
    
    instock = request.GET.get('instock')
    price_from = request.GET.get('price_from', 0)
    price_to = request.GET.get('price_to', 1000)
    sorting = request.GET.get('sorting', '-date_added')

    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))\
        .filter(price__gte=price_from).filter(price__lte=price_to)
    
    if instock:
        # GreaterThanEqual to 1 products available in store
        products = products.filter(num_available__gte=1)

    context = {
        'query': query,
        'products': products.order_by(sorting),
        'instock': instock,
        'price_from': price_from,
        'price_to': price_to,
        'sorting': sorting,
    }
    return render(request, 'search.html', context)

def store_detail(request, slug):
    """
    Renders the details of a specific store using as a parameter the slug (stringify id)
    Params:
        -slug:[String] A string-like id
    Return:
        -[Render] Renders the store_detail.html
    """
    store = get_object_or_404(Store, slug=slug)

    store.num_visits += 1
    store.last_visit = datetime.now()
    store.save()

    owned_stores = utils.get_owned_stores(request)

    categories = store.categories.all()
    products = store.products.all()

    category_form = AddCategoryForm(stores=owned_stores)

    context = {
        'store': store,
        'products': products,
        'categories': categories,
        'owned_stores': owned_stores,
        'category_form': category_form,
    }

    return render(request, 'store_detail.html', context)

def product_detail(request, category_slug, slug):
    """
    Return details about a specific product according to a request
    Params:
        - category_slug:[String] A specific ID-like string for a specific category
        - slug: [String]  A specific ID-like string for a specific product
    Return:
        -[Render]: Return a product_detail.html containing information about a specific product
    """

    product = get_object_or_404(Product, slug=slug)
    product.num_visits += 1
    product.last_visit = datetime.now()
    product.save()

    # Add review
    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars', 3)
        content = request.POST.get('content', '')

        review = ProductReview.objects.create(product=product, user=request.user, stars=stars, content=content)

        return redirect('product_detail', category_slug=category_slug, slug=slug)
    #

    related_products = list(product.category.products.all().exclude(id=product.id))
    if (len(related_products) >= 3):
        related_products = random.sample(related_products, 3)

    imagesstring = "{'thumbnail': '%s', 'image': '%s'}," %(product.thumbnail.url, product.image.url)
    
    # for image in product.images.all():
        # imagesstring += ("{'thumbnail': '%s', 'image': '%s'}," %(image.thumbnail.url, image.image.url))

    cart = Cart(request)
    if cart.has_product(product.id):
        product.in_cart = True
    else:
        product.in_cart = False

    owned_stores = utils.get_owned_stores(request)

    product_form = EditProductForm(instance=product, stores=owned_stores)

    context = {
        'product': product,
        'imagesstring': imagesstring,
        'related_products': related_products,
        'owned_stores': owned_stores,
        'product_form': product_form,
    }

    return render(request, 'product_detail.html', context)

def category_detail(request, slug):
    """
    Renders specific details of a category
    Params:
        -slug:[String] A specified id-like of a category
    Return:
        -[Render]: Renders the category_detail.html according to the category has been defined into the slug variable
    """
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    owned_stores = utils.get_owned_stores(request)

    category_form = EditCategoryForm(instance=category, stores=owned_stores)
    product_form = AddProductForm(stores=owned_stores)

    context = {
        'category': category,
        'products': products,
        'owned_stores': owned_stores,
        'category_form': category_form,
        'product_form': product_form,
    }

    return render(request, 'category_detail.html', context)