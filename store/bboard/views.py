import json

from django.http import HttpResponse
from django.urls import reverse_lazy

from .services.services import get_userprofile
from .services.cart import add_to_cart
from django.shortcuts import render
from .models import Product, Category,Cart, OrderLine, UserProfile, User, TypeUserProfile
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View, DeleteView
from .forms import CategoryForm, ProductForm

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
    error = ""
    if request.POST:
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        password_2 = request.POST.get("password_2")
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        address = request.POST.get("address")
        user = User.objects.filter(username = email)
        if user:
            error = "User already exists"
        elif password != password_2:
            error= "Password mismatch"
        else:
            User.objects.create_user(email, email, password)
            user = authenticate(request, username=email, password=password)
            type = TypeUserProfile.objects.get(name = 'customer')
            UserProfile.objects.create(user = user, name = name, surname = surname, user_address = address, email = email, id_type_user_profile =type)

            auth_login(request, user)
            return redirect("index")


    return render(request, 'bboard/basis/registration.html', {'error': error, 'user': user})


def logout(request):
    django_logout(request)
    return redirect("index")


def product(request):
    products = Product.objects.all()
    user = get_userprofile(request)

    return render(request,'bboard/basis/products/product.html', {'products':products,'user':user})


class ProductCreateView(View):
    def get(self, request):
        form = ProductForm
        user = get_userprofile(request)
        return render(request, 'bboard/basis/products/create.html', {'form': form, 'user': user})
    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            error = form.errors
            user = get_userprofile(request)
            return render(request, 'bboard/basis/products/create.html', {'form': form, 'user': user, 'error':error})


def product_from_category(request, id):
    user = get_userprofile(request)
    products = Product.objects.filter(id_category=id)
    return render(request, 'bboard/basis/products/product.html', {'products': products,'user':user})


class ProductUpdateView(View):
    def get(self, request, id):
        product= Product.objects.get(id = id)
        form = ProductForm(instance=product)
        user = get_userprofile(request)
        return render(request, 'bboard/basis/products/update.html', {'form': form, 'user': user, 'id': id})
    def post(self, request, id):
        product = Product.objects.get(id=id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            error = form.errors
            user = get_userprofile(request)
            return render(request, 'bboard/basis/products/update.html', {'form': form, 'user': user, 'error': error, 'id': id})


class ProductDeleteView(View):
    def get(self, request, id):
        product= Product.objects.get(id = id)
        user = get_userprofile(request)
        return render(request, 'bboard/basis/products/delete.html', {'user': user, 'id': id})
    def post(self, request, id):
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('index')


class ProductDetailView(View):
    def get(self, request, id):
        product= Product.objects.get(id = id)
        user = get_userprofile(request)
        return render(request, 'bboard/basis/products/details.html', {'product': product, 'user': user})

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
    context_object_name = 'category'


class CartView(View):
    def get(self, request):
        user = get_userprofile(request)

        try:
            cart = Cart.objects.get(id_customer=user)
        except:
            cart = Cart.objects.create(id_customer=user)

        order_lines = OrderLine.objects.filter(id_cart = cart)
        return render(request, 'bboard/basis/cart.html', {'user': user, 'order_lines': order_lines})

    def post(self, request):
        if request.is_ajax():
            add_to_cart(request)
            return HttpResponse(json.dumps("Success"), content_type="application/json")

        else:
            add_to_cart(request)
            return redirect('cart')


class CartDeleteView(View):
    def post(self, request):
        user = get_userprofile(request)
        cart = Cart.objects.get(id_customer=user)
        order_lines = OrderLine.objects.filter(id_cart=cart)
        for line in order_lines:
            line.delete()
        return redirect('cart')


class SearchView(View):
    def post(self, request):
        search_query = request.POST.get("search_query")
        search_query = search_query.lower()
        product_list = []
        products = Product.objects.all()
        user = get_userprofile(request)

        for product in products:
            name = product.name.lower()
            flag = name.find(search_query)
            if flag != -1:
                product_list.append(product)
            else:
                description = product.description.lower()
                flag = description.find(search_query)
                if flag != -1:
                    product_list.append(product)
        return render(request, 'bboard/basis/search.html', {'user': user, 'products': product_list})

@login_required(login_url="signin")
def purchase(request):
    user = get_userprofile(request)
    return render(request,'bboard/basis/purchase.html',{'user':user})