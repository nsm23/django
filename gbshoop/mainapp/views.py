from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.crypto import random

from mainapp.models import ProductCategory, Product

def index(request):
    cont = {
        'page': 'Home'
    }
    return render(request, 'mainapp/index.html', cont)


def get_menu():
    return ProductCategory.objects.all()


def products(request):
    hot_product = get_hot_product()
    cont = {
        'page': 'Products',
        'categories': get_menu(),
        'same_products': same_products(hot_product),
        'hot_product': hot_product,
        }

    return render(request, 'mainapp/products.html', cont)


def get_hot_product():
    product_id = Product.get_items().values_list('id', flat=True)
    rnd_id = random.choice(product_id)
    return Product.objects.get(pk=rnd_id)


def same_products(hot_product):
    return Product.get_items().filter(category=hot_product.category). \
               exclude(pk=hot_product.pk)[:3]


def contact(request):
    locations = [
        {'city': 'Moscow',
         'phone': '+7 495 777 55 77',
         'email': 'moscow@gbshop.ru',
         'address': 'В пределах МКАД '},
        {'city': 'Tver',
         'phone': '+7 818 777 55 77',
         'email': 'tver@gbshop.ru',
         'address': 'В пределах города '},
        {'city': 'Chelyabinsk',
         'phone': '+7 351 777 55 77',
         'email': 'chlb@gbshop.ru',
         'address': 'В пределах города '},
    ]
    cont = {
        'page': 'Contact',
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', cont)


def category(request, pk):
    page_num = request.GET.get('page', 1)
    if pk == 0:
        category = {'pk': 0, 'name': 'все'}
        products = Product.objects.all()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = category.product_set.filter(is_active=True)

    products_paginator = Paginator(products, 3)
    try:
        products = products_paginator.page(page_num)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)

    cont = {
        'page_title': 'products category',
        'category': category,
        'products': products,
        'categories': get_menu(),
    }
    return render(request, 'mainapp/cat_products.html', cont)


def product_page(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cont = {
        'page': 'Product_page',
        'categories': get_menu(),
        'product': product,
        }

    return render(request, 'mainapp/product_page.html', cont)


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=pk).first()
        return JsonResponse(
            {'price': product and product.price or 0}
        )
