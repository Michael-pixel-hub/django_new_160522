from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Category, Product
from mainapp.services import get_basket, get_hot_product, get_same_product


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

            context = {
                'links_menu': links_menu,
                'category': {'name': 'все'},
                'products': Product.objects.all().order_by('price'),
                'basket': get_basket(request.user)
            }

            return render(request, "mainapp/products_list.html", context)

        else:

            context = {
                'links_menu': links_menu,
                'category': get_object_or_404(Category, pk=pk),
                'products': Product.objects.filter(category__pk=pk).order_by('price'),
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