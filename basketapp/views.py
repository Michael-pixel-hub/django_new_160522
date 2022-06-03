from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product
from django.http import HttpResponseRedirect


def basket_list(request):
    basket = Basket.objects.filter(user=request.user)

    context = {
        'basket': basket
    }

    return render(request, 'basketapp/list.html', context)


def basket_add(request, pk):
    product_item = get_object_or_404(Product, pk=pk)

    basket_item = Basket.objects.filter(user=request.user, product=product_item).first()

    if not basket_item:
        basket_item = Basket(product=product_item, user=request.user)

    basket_item.quantity += 1
    basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, pk):
    Basket.objects.filter(pk=pk).delete()
    return HttpResponseRedirect('')
