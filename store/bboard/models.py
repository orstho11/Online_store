from django.db import models


from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class TypeUserProfile(models.Model):
    name = models.CharField(max_length=50)



class UserProfile(models.Model):
    #ID_user_profile = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=17)
    id_type_user_profile = models.ForeignKey(TypeUserProfile, on_delete=models.CASCADE)
    class Meta:
        db_table = "customer"

    def __str__(self):
        return self.surname + " " + self.name
class Category(models.Model):
    name = models.CharField(max_length=50)
    # ID default: ID_user_profile = models.AutoField(primary_key=True)
    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    def __str__(self):
        return self.surname + " " + self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    amount = models.IntegerField()
    price = models.FloatField()
    #thumbnail = models.ImageField(upload_to='/thumbnail')
    thumbnail = models.ImageField()
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    id_author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Cart(models.Model):
    id_customer = models.OneToOneField(UserProfile, on_delete=models.CASCADE)


class OrderLine(models.Model):
    id_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product =models.ForeignKey(Product, on_delete=models.CASCADE)
    number_of_products = models.IntegerField()
    product_price = models.FloatField()

class Status(models.Model):
    name = models.CharField(max_length=255)


class Order(models.Model):
    id_user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    total = models.FloatField()
    delivery_address = models.CharField(max_length=255)
    date_of_submission = models.DateField()
    id_status = models.ForeignKey(Status,on_delete=models.CASCADE)
