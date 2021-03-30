from django.urls import reverse_lazy

from .services.services import get_userprofile
from django.shortcuts import render
from .models import Product, Category, Purchase
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, View, FormView, DeleteView
from .forms import CategoryForm

# Create your views here.

def bboard(request):
    user = get_userprofile(request)
    products = Product.objects.all()
    categories = Category.objects.all()[:2]
    return render(request,'bboard/basis/index.html', {'user':user, 'products':products,'categories':categories})


def signin(request):
    user = get_userprofile(request)
    login_error = ""
    if request.POST:
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("index")

        else:
            login_error = "Incorrect password or user name. Try again."


    return render(request,'bboard/basis/signin.html',{'login_error':login_error,'user':user})

def registration(request):
    user = get_userprofile(request)
    return render(request,'bboard/basis/registration.html',{'user':user})


def logout(request):
    django_logout(request)
    return redirect("index")


def product(request):
    products = Product.objects.all()
    user = get_userprofile(request)

    return render(request,'bboard/basis/product.html', {'products':products,'user':user})


def product_from_category(request, id):
    user = get_userprofile(request)
    products = Product.objects.filter(id_category=id)
    return render(request, 'bboard/basis/product.html', {'products': products,'user':user})


def category(request):
    user = get_userprofile(request)
    categories = Category.objects.all()
    return render(request,'bboard/basis/category/category.html', {'categories':categories,'user':user})


class CategoryCreateView(View):
    def get(self, request):
        form = CategoryForm
        user = get_userprofile(request)
        return render(request, 'bboard/basis/category/create.html', {'form': form, 'user': user})
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category')
        else:
            error = form.errors
            user = get_userprofile(request)
            return render(request, 'bboard/basis/category/create.html', {'form': form, 'user': user, 'error':error})
class CategoryUpdateView(View):
    def get(self, request, id):
        category = Category.objects.get(id = id)
        form = CategoryForm(instance=category)
        user = get_userprofile(request)
        return render(request, 'bboard/basis/category/update.html', {'form': form, 'user': user, 'id': id})
    def post(self, request, id):
        category = Category.objects.get(id=id)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category')
        else:
            error = form.errors
            user = get_userprofile(request)
            return render(request, 'bboard/basis/category/update.html', {'form': form, 'user': user, 'error': error, 'id': id})


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'bboard/basis/category/delete.html'
    success_url = reverse_lazy('category')


@login_required(login_url="signin")
def purchase(request):
    user = get_userprofile(request)
    return render(request,'bboard/basis/purchase.html',{'user':user})