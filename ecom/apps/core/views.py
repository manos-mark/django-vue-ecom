from django.shortcuts import render

from apps.store.models import Product, Category, Store, StoreAdmin
from apps.userprofile.models import Userprofile
from django.contrib.auth.models import User


def frontpage(request):
    stores = Store.objects.filter(is_activated=True).order_by('-num_visits')
    products = Product.objects.filter(is_featured=True)
    featured_categories = Category.objects.filter(is_featured=True)
    popular_products = Product.objects.all().order_by('-num_visits')[0:4]
    recently_viewed_products = Product.objects.all().order_by('-last_visit')[0:4]

    owned_stores = []
    if not request.user.is_anonymous:
        user = User.objects.get(id=request.user.id)
        store_admins = StoreAdmin.objects.filter(user=user)
        
        for admin in store_admins:
            owned_stores.append(admin.store)

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