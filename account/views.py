from django.contrib.auth import authenticate, login, logout

from django.contrib.auth import forms
from django.http import request
from django.views.generic import FormView
from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import SignUpForm, LoginForm
from django.contrib import messages
#
from .models import User
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


# Create your views here.


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            messages.success(request, 'Your Account Created Successfully.')
            form.save()
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# class LoginView(FormView):
#     form_class = LoginForm
#     success_url = '/user'
#     template_name = "userlogin.html"

#     def form_valid(self, form):
#         request = self.request
#         email = form.cleaned_data.get('email')
#         password = form.cleaned_data.get('password')
#         user = authenticate(request, email=email, password=password)
#         print(user)
#         if user:
#             login(request, user)
#             print(user)
#             return redirect('/user/')
#         else:
#             return redirect('/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/account/login/')


# def password_reset(request):
#     if request.method == "POST":
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data['email']
#             associated_users = User.objects.filter(Q(email=data))
#             if associated_users.exists():
#                 for user in associated_users:
#                     subject = "Password Reset Requested"
#                     email_template_name = ''
#                     c = {
#                         'email': user.email,
#                         'domain': '127.0.0.1:8000',
#                         'site_name': 'Website',
#                         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                         "user": user,
#                         'token': default_token_generator.make_token(user),
#                         'protocol': 'http',
#                     }
#                     email = render_to_string(email_template_name, c)

#     form = PasswordResetForm()
#     return render(request, "password_reset.html", {"form": form})


def user_login(request):
    if request.method == 'POST':
        # form = AuthenticationForm(request=request, data=request.POST)
        print('Hello')
        print(request.POST)

        uname = request.POST.get('username')
        upass = request.POST.get('password')
        user = authenticate(username=uname, password=upass)
        print(user)
        if user is not None:
            login(request, user)
            # return redirect('/user/userread')
        else:
            messages.info(request, "You are now logged in.")
            # return redirect('/')
    form = AuthenticationForm()
    return render(request, 'userlogin.html', {'form': form})
