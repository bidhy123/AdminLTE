from django import forms
from django.forms import widgets
# from django.db.models.fields import CharField
# from django.forms import fields
# from django.forms.widgets import Widget
from . models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'address', 'email', 'password')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'password': forms.PasswordInput(render_value=True, attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError('Enter more than or equal 6 character')
        return password
