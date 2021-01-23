from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Product, Category

def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    context = {
        'query': query,
        'products': products
    }
    return render(request, 'search.html', context)

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)

    imagesstring = "{'thumbnail': '%s', 'image': '%s'}," %(product.thumbnail.url, product.image.url)
    
    for image in product.images.all():
        imagesstring += ("{'thumbnail': '%s', 'image': '%s'}," %(image.thumbnail.url, image.image.url))

    context = {
        'product': product,
        'imagesstring': imagesstring
    }

    return render(request, 'product_detail.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)

    products = category.products.all()

    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'category_detail.html', context)