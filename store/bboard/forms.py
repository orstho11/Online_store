from django import forms
from .models import Category

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
