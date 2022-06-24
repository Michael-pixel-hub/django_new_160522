from django.shortcuts import render, get_object_or_404
from authapp.models import ShopUser
from mainapp.models import Category, Product
from django.contrib.auth.decorators import user_passes_test
from authapp.forms import UserRegisterForm
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from adminapp.forms import UserAdminEditForm, CategoryEditForm
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin


class AccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = UserRegisterForm()

    context = {
        'title': title,
        'update_form': user_form
    }
    return render(request, 'adminapp/user_update.html', context)


class UserListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    paginate_by = 2


    # @method_decorator(user_passes_test(lambda u: u.is_superuser))
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)


class UserUpdateView(AccessMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = UserAdminEditForm

    def get_success_url(self):
        return reverse('adminapp:user_update', args=[self.kwargs.get('pk')])


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))

    context = {
        'title': title,
        'user_to_delete': user
    }
    return render(request, 'adminapp/user_delete.html', context)


class CategoryCreateView(AccessMixin, CreateView):
    model = Category
    # form_class = CategoryEditForm
    success_url = reverse_lazy('adminapp:categories_read')
    template_name = 'adminapp/category_update.html'
    fields = ('name', 'description',)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'
    categories_list = Category.objects.all()
    context = {
        'title': title,
        'categories_list': categories_list
    }
    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'категории/редактирование'
    edit_category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        edit_form = CategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_update', args=[edit_category.pk]))
    else:
        edit_form = CategoryEditForm(instance=edit_category)

    context = {
        'title': title,
        'update_form': edit_form
    }
    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'категории/удаление'
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.is_active = False
        category.save()
        return HttpResponseRedirect(reverse('adminapp:categories_read'))

    context = {
        'title': title,
        'category_to_delete': category
    }
    return render(request, 'adminapp/category_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    return None


class ProductListView(AccessMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return context_data

    def get_queryset(self):
        return super().get_queryset().filter(category_id=self.kwargs.get('pk'))


class ProductDetailView(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


@user_passes_test(lambda u: u.is_superuser)
def product_update(request):
    return None


class ProductDeleteView(AccessMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        category_pk = self.get_object().category_id
        return reverse('adminapp:products', args=[category_pk])

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())