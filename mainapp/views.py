from django.shortcuts import render
from geekshop.settings import BASE_DIR
import json


def index(request):
    context = {
        'title': 'Магазин',
    }
    return render(request, "mainapp/index.html", context)


def products(request):
    with open(BASE_DIR/"mainapp/json/content.json", 'r', encoding='utf-8') as file:
        context = json.load(file)
    return render(request, "mainapp/products.html", context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, "mainapp/contact.html", context)