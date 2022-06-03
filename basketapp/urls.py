from django.urls import path
from basketapp.views import basket_list, basket_add, basket_remove

app_name = 'basketapp'

urlpatterns = [
    path('', basket_list, name='view'),
    path('add/<int:pk>/', basket_add, name='add'),
    path('remove/<int:pk>)/', basket_remove, name='remove'),
]