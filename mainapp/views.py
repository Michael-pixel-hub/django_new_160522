from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Category, Product


def index(request):
    context = {
        'title': 'Магазин',
        'products': Product.objects.all()[0:4]
    }
    return render(request, "mainapp/index.html", context)


def products(request, pk=None):
    link_menu = Category.objects.all()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 1:
            category = {'name': 'все'}
            products = Product.objects.all().order_by('price')

            context = {
                'link_menu': link_menu,
                'category': category,
                'products': products,
                'basket': basket
            }

            return render(request, "mainapp/products_list.html", context)

        else:
            category = get_object_or_404(Category, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

            context = {
                'link_menu': link_menu,
                'category': category,
                'products': products,
                'basket': basket
            }

            return render(request, "mainapp/products_list.html", context)

    products = Product.objects.all()

    context = {
        'link_menu': link_menu,
        'products': products,
        'basket': basket,
        'hot_product': Product.objects.all().order_by('?').first()
    }
    return render(request, "mainapp/products.html", context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, "mainapp/contact.html", context)
