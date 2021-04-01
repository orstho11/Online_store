from django.urls import path
from . import views

urlpatterns = [
    path('', views.bboard, name = 'index'),

    path('category', views.category, name = 'category'),
    path('category/create', views.CategoryCreateView.as_view(),name = 'category_create'),
    path('category/<int:id>/update', views.CategoryUpdateView.as_view(),name = 'category_update'),
    path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(),name = 'category_delete'),

    path('purchase', views.purchase, name = 'purchase'),

    path('product', views.product, name = 'product'),
    path('product/create', views.ProductCreateView.as_view(), name = 'product_create'),
    path('product/<int:id>', views.product_from_category, name = 'product_from_category'),
    path('product/<int:id>/update', views.ProductUpdateView.as_view(), name = 'product_update'),
    path('product/<int:id>/detail', views.ProductDetailView.as_view(), name = 'product_detail'),
    path('product/<int:id>/delete', views.ProductDeleteView.as_view(), name='product_delete'),
    path('signin', views.signin, name = 'signin'),
    path('registration', views.registration, name = 'registration'),
    path('logout', views.logout, name = 'logout'),
    path('cart', views.Cart.as_view(), name = 'cart'),
]