from django.contrib import admin
from .models import Category, Product, ProductType, Author, TypeUserProfile, UserProfile
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(Author)
admin.site.register(TypeUserProfile)
admin.site.register(UserProfile)
