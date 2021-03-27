from django.urls import path
from . import views

urlpatterns = [
    path('', views.bboard, name = 'index'),
    path('product', views.product, name = 'product'),
    path('category', views.category, name = 'category'),
    path('purchase', views.purchase, name = 'purchase'),
    path('product/<int:id>', views.product_from_category, name = 'product_from_category'),
    path('signin', views.signin, name = 'signin'),
    path('registration', views.registration, name = 'registration'),
    path('logout', views.logout, name = 'logout'),
]