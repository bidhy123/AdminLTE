from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    path("", views.user_login, name="login"),
    path("sign_up", views.sign_up, name="sign_up"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),

    path("user_logout", views.user_logout, name="user_logout"),
    path("password_reset", views.password_reset_request, name="password_reset"),

]
