import json

from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy

from .services.services import get_userprofile
from .services.cart import add_to_cart
from django.shortcuts import render
from .models import Product, Category,Cart, OrderLine, UserProfile, User, TypeUserProfile, Status, Order
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View, DeleteView
from .forms import CategoryForm, ProductForm, ProductFilterForm, OrderForm
from .services.weather import get_weather
from django.core.paginator import Paginator
import datetime
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin



class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        user = get_userprofile(self.request)
        return user.id_type_user_profile.name == 'admin'

    def handle_no_permission(self):
        return redirect('index')





# Create your views here.

def bboard(request, **kwargs):
    user = get_userprofile(request)
    products = Product.objects.all()
    categories = Category.objects.all()[:2]
    weather = get_weather(user)
    form = ProductFilterForm(request.GET)
    product_per_page = 2
    if form.is_valid():
        if form.cleaned_data['min_price']:
           products = products.filter(price__gte= form.cleaned_data['min_price'])
        if form.cleaned_data['max_price']:
           products = products.filter(price__lte= form.cleaned_data['max_price'])
        if form.cleaned_data['product_per_page']:
           product_per_page = form.cleaned_data['product_per_page']
    page_number = request.GET.get('page', 1)
    paginator = Paginator(products, product_per_page)
    page = paginator.get_page(page_number)
    d = request.GET.copy()

    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]

    try:
        d.pop('page')
    except:
        pass
    t = d.urlencode()

    return render(request,'bboard/basis/index.html', {'user':user, 'products':page, 'page': page, 'categories':categories, 'weather': weather, 'form': form, 'param_page': t})


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
        country = request.POST.get("country")
        city = request.POST.get("city")
        zip_code = int(request.POST.get("zip_code"))
        street = request.POST.get("street")
        user = User.objects.filter(username = email)
        if user:
            error = "User already exists"
        elif password != password_2:
            error= "Password mismatch"
        else:
            User.objects.create_user(email, email, password)
            user = authenticate(request, username=email, password=password)
            type = TypeUserProfile.objects.get(name = 'customer')
            UserProfile.objects.create(user = user, name = name, surname = surname, country = country, email = email,
                                       id_type_user_profile =type, zip_code= zip_code, street = street, city = city)

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


class ProductCreateView(IsAdminMixin, View):
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


class ProductUpdateView(IsAdminMixin, View):
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


class ProductDeleteView(IsAdminMixin, View):
    def get(self, request, id):
        product= Product.objects.get(id = id)
        user = get_userprofile(request)
        return render(request, 'bboard/basis/products/delete.html', {'user': user, 'id': id})
    def post(self, request, id):
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('index')


class ProductDetailView(PermissionRequiredMixin, View):
    permission_required = ['bboard.view_product'] #PermissionRequiredMixin and permission_required added for beingable to addaccess rights in admin tool. In admin tool: 1. Create group. 2. assigned what is accesable for the created group
    def get(self, request, id):
        product= Product.objects.get(id = id)
        user = get_userprofile(request)
        return render(request, 'bboard/basis/products/details.html', {'product': product, 'user': user})

def category(request):
    user = get_userprofile(request)
    categories = Category.objects.all()
    return render(request,'bboard/basis/category/category.html', {'categories':categories,'user':user})




class CategoryCreateView(IsAdminMixin, View):
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
class CategoryUpdateView(IsAdminMixin, View):
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


class CategoryDeleteView(IsAdminMixin, DeleteView):
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


class BuyView(View):
    def get(self, request):
        user = get_userprofile(request)
        cart = Cart.objects.get(id_customer=user)
        order_lines = OrderLine.objects.filter(id_cart=cart)
        return render(request, 'bboard/basis/buy.html', {'user': user, 'order_lines': order_lines})

    def post(self, request):
        user = get_userprofile(request)
        cart = Cart.objects.get(id_customer=user)
        order_lines = OrderLine.objects.filter(id_cart=cart)
        delivery_address = request.POST.get("delivery_address")
        status = Status.objects.get(name = 'In progress')
        total = 0
        for line in order_lines:
           total += line.product_price * line.number_of_products
        order = Order.objects.create(id_user_profile=user, total= total, delivery_address=delivery_address, date_of_submission= datetime.datetime.now(), id_status=status)

        for line in order_lines:
            OrderLine.objects.filter(id=line.id).update(id_order=order, id_cart = None)
            order_line = OrderLine.objects.get(id=line.id)
            product = Product.objects.get(id = order_line.product.id)
            Product.objects.filter(id= product.id).update(amount=product.amount-order_line.number_of_products)
        return redirect('order')


class CartDeleteView(View):
    def post(self, request):
        user = get_userprofile(request)
        cart = Cart.objects.get(id_customer=user)
        order_lines = OrderLine.objects.filter(id_cart=cart)
        for line in order_lines:
          #  line.delete()
            OrderLine.objects.filter(id=line.id).update(id_cart= None)
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


def search_ajax(request):
    if request.method == 'POST':
        search_body = json.loads(request.body).get('searchQuery')
        products = Product.objects.filter(name__icontains=search_body) | Product.objects.filter(description__icontains=search_body)
        data = products.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url="signin")
def order(request):
    user = get_userprofile(request)
    orders = Order.objects.filter(id_user_profile=user)

    return render(request,'bboard/basis/order/order.html',{'user':user, 'orders': orders})


def order_details(request, id):
    order = Order.objects.get(id = id)
    order_lines = OrderLine.objects.filter(id_order= order)
    user = get_userprofile(request)
    return render(request, 'bboard/basis/order/order_details.html', {'user': user, 'order_lines': order_lines})


class OrderAdminView(IsAdminMixin, View):
    def get(self, request):
        user = get_userprofile(request)
        orders = Order.objects.all()
        return render(request, 'bboard/basis/order/admin_order.html', {'user': user, 'orders': orders})


class OrderAdminUpdate(IsAdminMixin, View):
    def get(self, request, id):
        order = Order.objects.get(id = id)
        form = OrderForm(instance=order)
        user = get_userprofile(request)
        return render(request, 'bboard/basis/order/admin_order_update.html', {'user': user, 'form': form, 'id': id})

    def post(self, request, id):
        order = Order.objects.get(id=id)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin_order')
        else:
            error = form.errors
            user = get_userprofile(request)
            return render(request, 'bboard/basis/order/admin_order_update.html', {'user': user, 'form': form, 'id': id, 'error': error})