from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    path("", views.user_login, name="login"),
    path("sign_up", views.sign_up, name="sign_up"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),

    path("user_logout", views.user_logout, name="user_logout"),
    path('password_reset', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    #     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
    #          name='password_reset_done'),
    #     path('password/<uidb64>/<token>/',
    #          auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #     path('password/done/<idb64>/<token>/', auth_views.PasswordResetCompleteView.as_view(),
    #          name='password_reset_complete'),
    #     path('', views.LoginView.as_view(), name='login'),
]
