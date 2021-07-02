from django import forms
from django.forms import widgets

from . models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('categoryname', 'vendor')
        widgets = {
            'categoryname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter  Categoryname'}),
            'vendor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter vendor name'}),
        }
