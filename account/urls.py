from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    path('sign_up', views.sign_up, name='sign_up'),
    #     path('', views.LoginView.as_view(), name='login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('', views.user_login, name='login'),


    path('password_reset', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/done/<idb64>/<token>/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
