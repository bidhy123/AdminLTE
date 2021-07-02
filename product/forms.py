from django import forms
from . models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('productname', 'productquantity',
                  'productstock', 'productprice')
        widgets = {
            'productname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'product name'}),
            'productquantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'product quantity'}),
            'productstock': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'product stock'}),
            'productprice': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'product price'}),
        }
