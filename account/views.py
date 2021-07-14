from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import SignUpForm, UserImageForm, UserAddForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from .models import User
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm, PasswordChangeForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

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
            return redirect('account:userread')
        else:
            print("??????????????????")
            messages.warning(request, "Email or password invalid.")
            return redirect('/')
    form = AuthenticationForm()
    return render(request, 'userlogin.html', {'form': form})


# @login_required(login_url="/")
# def useradd(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             User.full_name = form.cleaned_data['name']
#             User.address = form.cleaned_data['address']
#             User.email = form.cleaned_data['email']
#             User.password = form.cleaned_data['password1']
#             useradded = form.save(commit=False)
#             useradded.save()
#             form = SignUpForm()
#             messages.add_message(request, messages.SUCCESS,
#                                  'your Account has been registered Successfully.')
#         else:
#             print('form is not valid')

#     else:
#         form = SignUpForm()
#     return render(request, 'account/useradd.html', {'form': form})

@login_required(login_url="/")
def useradd(request):
    if request.method == 'POST':
        print(request.POST)
        print("<><>><<>")
        form = UserAddForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["full_name"]
            address = form.cleaned_data["address"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User(email=email,
                        full_name=name,
                        address=address,
                        password=password,
                        )
            user.set_password(password)
            user.save()
            messages.success(request, 'Your Account Created Successfully.')
        else:
            messages.error(request, "registration failed, try again.")
    else:
        form = UserAddForm()
    return render(request, 'account/useradd.html', {'form': form})


@login_required(login_url="/")
def userread(request):
    user = User.objects.all()
    return render(request, 'account/userread.html', {'user': user})


@login_required(login_url="/")
def user_update(request, id):
    if request.method == 'POST':
        updt = User.objects.get(pk=id)
        form = SignUpForm(request.POST, instance=updt)
        if form.is_valid():
            form.save()
        else:
            print('invalid')
    updt = User.objects.get(pk=id)
    form = SignUpForm(instance=updt)
    messages.add_message(request, messages.SUCCESS,
                         'Your Account Has Been Updated.')
    return render(request, 'account/userupdate.html', {'form': form})


@login_required(login_url="/")
def user_delete(request, id):
    if request.method == 'POST':
        delt = User.objects.get(pk=id)
        delt.delete()
        messages.add_message(request, messages.SUCCESS,
                             'Your Account Has Been Deleted.')
        return redirect("/userread")


def profile(request):
    if request.method == "POST":
        form = UserImageForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Picture Updated")
            return redirect("account:profile")
        else:
            messages.error(request, "Could not upload image, try again.")
    else:
        form = UserImageForm()
    return render(request, "account/profile.html", {"form": form})


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = 'password_reset_email.html'
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
                    return redirect('/password_reset/done/')
    form = PasswordResetForm()
    return render(
        request=request,
        template_name="password_reset.html",
        context={"form": form},
    )


def change_pass(request):
    if request.method == "POST":
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Password changed successfully.")
            update_session_auth_hash(request, fm.user)
    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request, "account/changepass.html", {"form": fm})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
