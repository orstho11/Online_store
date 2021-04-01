from django import forms
from .models import Category, Product

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