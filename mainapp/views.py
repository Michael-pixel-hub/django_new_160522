from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Category, Product
from mainapp.services import get_basket, get_hot_product, get_same_product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    context = {
        'title': 'Магазин',
        'products': Product.objects.all()[0:4]
    }
    return render(request, "mainapp/index.html", context)


def products(request, pk=None):
    links_menu = Category.objects.all()

    if pk is not None:
        if pk == 1:
            products_list = Product.objects.all().order_by('price')
            category = {'name': 'все', 'pk': 1}

        else:
            products_list = Product.objects.filter(category__pk=pk).order_by('price')
            category = get_object_or_404(Category, pk=pk)

        page = request.GET.get('page')
        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
            'basket': get_basket(request.user)
        }

        return render(request, "mainapp/products_list.html", context)

    context = {
        'links_menu': links_menu,
        'basket': get_basket(request.user),
        'same_product': get_same_product(get_hot_product()),
        'hot_product': get_hot_product()
    }
    return render(request, "mainapp/products.html", context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, "mainapp/contact.html", context)


def product(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    links_menu = Category.objects.all()

    context = {
        'product': product_item,
        'basket': get_basket(request.user),
        'links_menu': links_menu,
    }

    return render(request, 'mainapp/product.html', context)