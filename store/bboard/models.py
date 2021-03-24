from django.db import models


from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Customer(models.Model):
    #ID_user_profile = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=17)

    class Meta:
        db_table = "customer"

    #def __str__(self):
     #   return self.surname + " " + self.name
class Category(models.Model):
    name = models.CharField(max_length=50)
    # ID default: ID_user_profile = models.AutoField(primary_key=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    amount = models.IntegerField()
    price = models.FloatField()

    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Purchase(models.Model):
    id_customer = models.ForeignKey(Customer,on_delete=models.CASCADE)

class Purchase_Position(models.Model):
    amount = models.IntegerField()
    id_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    id_purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE)
