from django.db import models
from account.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

User = get_user_model()


class SignUpForm(forms.ModelForm):
    full_name = forms.CharField()
    address = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Conform Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'address',)

        def clean_email(self):  # Verify email is available.

            email = self.cleaned_data.get('email')
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError('email is taken')
            return email

        def clean_password2(self):  # Verify both passwords match.
            password1 = self.cleaned_data.get('Password1')
            password2 = self.cleaned_data.get('Password2')

            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("your passwords don't match")
            return password2

        def save(self, commit=True):
            user = super(SignUpForm, self).save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            return user


"""
 A form for creating new users. Includes all the required fields, plus a repeated password.
"""


class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Conform Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'address',)

    def clean_password2(self):  # Verify both passwords match.
        password1 = self.cleaned_data.get('Password1')
        password2 = self.cleaned_data.get('Password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("your passwords don't match")
        return password2

    def save(self, commit=True):  # save the provided passwd in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'full_name', 'address',
                  'password', 'active', 'admin']

    def clean_password(self):
        return self.initial['password']


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)


# class ChangePasswordForm(forms.Form):
#     new_password = forms.CharField(widget=forms.PasswordInput)
#     password = forms.CharField(widget=forms.PasswordInput)
