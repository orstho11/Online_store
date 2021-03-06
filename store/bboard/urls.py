from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.bboard, name = 'index'),

    path('category', views.category, name = 'category'),
    path('category/create', views.CategoryCreateView.as_view(),name = 'category_create'),
    path('category/<int:id>/update', views.CategoryUpdateView.as_view(),name = 'category_update'),
    path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(),name = 'category_delete'),

    path('order', views.order, name = 'order'),
    path('order/<int:id>/detail', views.order_details, name = 'order_details'),
    path('product', views.product, name = 'product'),
    path('product/create', views.ProductCreateView.as_view(), name = 'product_create'),
    path('product/<int:id>', views.product_from_category, name = 'product_from_category'),
    path('product/<int:id>/update', views.ProductUpdateView.as_view(), name = 'product_update'),
    path('product/<int:id>/detail', views.ProductDetailView.as_view(), name = 'product_detail'),
    path('product/<int:id>/delete', views.ProductDeleteView.as_view(), name='product_delete'),
    path('signin', views.signin, name = 'signin'),
    path('registration', views.registration, name = 'registration'),
    path('logout', views.logout, name = 'logout'),
    path('cart', views.CartView.as_view(), name = 'cart'),
    path('cart/delete', views.CartDeleteView.as_view(), name = 'cart_delete'),
    path('search', views.SearchView.as_view(), name = 'search'),
    path('buy', views.BuyView.as_view(), name = 'buy'),
    path('admin/order', views.OrderAdminView.as_view(), name = 'admin_order'),
    path('admin/order/<int:id>/update', views.OrderAdminUpdate.as_view(), name = 'admin_order_update'),
    path('product/search', csrf_exempt(views.search_ajax), name='product_search'),

]