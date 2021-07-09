from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.contrib.auth.tokens import default_token_generator
from .models import User
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.conf import settings
UserModel = get_user_model()

# Create your views here.


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account.'
    email_body = render_to_string(
        "activate.html",
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.id)),
            "token": generate_token.make_token(user),
        },)
    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email],
                         )
    email.send()


def sign_up(request):
    if request.method == 'POST':
        print(request.POST)
        print("<><>><<>")
        form = SignUpForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password1"]
            user_added = form.save(commit=False)
            # user_added.staff = True
            user_added.active = False
            user_added.set_password(password)
            user_added.save()
            send_activation_email(user_added, request)
            messages.success(request, 'Your Account Created Successfully.')
            return redirect('/')
        else:
            messages.error(request, "registration failed, try again.")
            return redirect('/sign_up')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Thank you for your email confirmation. Now you can login your account.')
        return redirect("/")
    else:
        return render(request, "activation_failed.html", {"user": user})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        print('Hello')
        print(request.POST)

        uname = request.POST.get('username')
        upass = request.POST.get('password')
        user = authenticate(username=uname, password=upass)
        print(user)
        if user:
            print("<><><><>>")
            login(request, user)
            messages.info(request, "Login Successfully.")
            return redirect('/user/userread')
        else:
            print("??????????????????")
            messages.warning(request, "Email or password invalid.")
            return redirect('/')
    form = AuthenticationForm()
    return render(request, 'userlogin.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/account/login/')


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = ''
                    c = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            'admin@example.com',
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse('invalid header found.')
                    return redirect('../../password_reset/done/')
    form = PasswordResetForm()
    return render(
        request=request,
        template_name="password_reset.html",
        context={"form": form},
    )
