from django.shortcuts import render

from apps.store.utils import get_owned_stores
from apps.store.models import Product, Category, Store


def frontpage(request):
    stores = Store.objects.filter(is_activated=True).order_by('-num_visits')
    products = Product.objects.filter(is_featured=True)
    featured_categories = Category.objects.filter(is_featured=True)
    popular_products = Product.objects.all().order_by('-num_visits')[0:4]
    recently_viewed_products = Product.objects.all().order_by('-last_visit')[0:4]

    owned_stores = get_owned_stores(request)

    context = {
        'stores': stores,
        'products': products,
        'featured_categories': featured_categories,
        'popular_products': popular_products,
        'recently_viewed_products': recently_viewed_products,
        'owned_stores': owned_stores
    }

    return render(request, 'frontpage.html', context)

def create_store(request):
    return render(request, 'create_store.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')