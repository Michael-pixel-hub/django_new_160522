import json

from django.core.management import BaseCommand

from mainapp.models import Category, Product

from django.conf import settings

from authapp.models import ShopUser

class Command(BaseCommand):

    @staticmethod
    def load_data_from_file(file_name):
        with open(f'{settings.BASE_DIR}/mainapp/json/{file_name}.json') as json_file:
            return json.load(json_file)

    def handle(self, *args, **options):
        Category.objects.all().delete()

        categories_list = self.load_data_from_file('categories')

        categories_batch = []

        for cat in categories_list:
            categories_batch.append(Category(
                name=cat['name'],
                description=cat['description']
            ))

        Category.objects.bulk_create(categories_batch)

        Product.objects.all().delete()

        products_list = self.load_data_from_file('products')

        for prod in products_list:
            _cat = Category.objects.get(name=prod.get('category'))
            prod['category'] = _cat

            Product.objects.create(**prod)

        shop_user = ShopUser.objects.create_superuser(username='django', email='geekbrains@gmail.com', age=23)
        shop_user.set_password('geekbrains')
        shop_user.save()