from django import forms
from .models import Category, Product, Order

class CategoryForm(forms.ModelForm):
    class Meta:
        model= Category
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'id_category': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'id_product_type': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'id_author': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )


        }

class ProductFilterForm(forms.Form):
    min_price = forms.IntegerField(label='price from:', required=False,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_price = forms.IntegerField(label='price to:', required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    CHOICES = (('2', '2'),('3', '3'), ('4', '4'))
    product_per_page = forms.ChoiceField(choices = CHOICES,label= 'Product per page', required=False, widget=forms.Select(attrs={'class': 'form-control'}))


class OrderForm(forms.ModelForm):
    class Meta:
        model= Order
        fields = ['id_status']

        widgets = {
            'id_status': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }