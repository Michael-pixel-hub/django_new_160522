from django.shortcuts import render
from mainapp.models import Category


def index(request):
    context = {
        'title': 'Магазин',
    }
    return render(request, "mainapp/index.html", context)


def products(request):
    context = {
        'link_menu': Category.objects.all()
    }
    return render(request, "mainapp/products.html", context)


def products_list(request, pk):
    context = {
        'link_menu': Category.objects.all()
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, "mainapp/contact.html", context)