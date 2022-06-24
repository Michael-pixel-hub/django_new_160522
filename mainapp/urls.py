from django.urls import path
from mainapp.views import products, product

app_name = 'products'

urlpatterns = [
    path('', products, name='products_hot_product'),
    path('<int:pk>/', products, name='product_list'),
    # path('<int:pk>/<int:page>/', products, name='page'),
    path('product/<int:pk>/', product, name='product_item'),
]