from .services.services import get_userprofile
from django.shortcuts import render
from .models import Product, Category, Purchase
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def bboard(request):
    user = get_userprofile(request)
    return render(request,'bboard/basis/index.html', {'user':user})


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
    return render(request,'bboard/basis/category.html', {'categories':categories,'user':user})

@login_required(login_url="signin")
def purchase(request):
    user = get_userprofile(request)
    return render(request,'bboard/basis/purchase.html',{'user':user})