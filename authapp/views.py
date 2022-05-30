from django.shortcuts import render, HttpResponseRedirect

from django.urls import reverse

from django.contrib import auth

from authapp.forms import UserLoginForm, UserRegisterForm, UserEditForm


def login(request):
    login_form = UserLoginForm(data=request.POST)
    if request.method == "POST" and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': login_form
    }

    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == "POST":
        register_form = UserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        register_form = UserRegisterForm()

    context = {
        'form': register_form
    }

    return render(request, 'authapp/register.html', context)


def edit(request):
    if request.method == "POST":
        edit_form = UserRegisterForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_form = UserEditForm()

    context = {
        'form': edit_form
    }

    return render(request, 'authapp/edit.html', context)
