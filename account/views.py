from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import forms
from django.http import request
from django.views.generic import FormView
from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from .models import User
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm


# Create your views her e.


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            messages.success(request, 'Your Account Created Successfully.')
            form.save()
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = "userlogin.html"

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print(user)
            return HttpResponseRedirect('/user/')
        else:
            print('hello')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/account/login/')


def password_reset(request):
    if request.method == "POST":
        fm = SetPasswordForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Password changed successfully.")
    else:
        fm = SetPasswordForm(user=request.user)
    return render(request, "changepass.html", {"form": fm})


# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         print('Hello')
#         if form.is_valid():
#             uname = form.cleaned_data.get('username')
#             upass = form.cleaned_data('password')
#             user = authenticate(username=uname, password=upass)
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect('/user/userread')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'userlogin.html', {'form': form})

# def forget_password(request):
#     return render(request)
