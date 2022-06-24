from basketapp.models import Basket
from mainapp.models import Product


def get_basket(user):
    basket = []
    if user.is_authenticated:
        basket = Basket.objects.filter(user=user)
    return basket


def get_hot_product():
    return Product.objects.all().order_by('?').first()


def get_same_product(product):
    return Product.objects.filter(category=product.category).exclude(pk=product.pk)
