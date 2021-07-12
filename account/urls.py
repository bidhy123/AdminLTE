from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    path("", views.user_login, name="login"),
    path("sign_up", views.sign_up, name="sign_up"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("user_logout", views.user_logout, name="user_logout"),
    path("profile/", views.profile, name="profile"),
    path("password_reset_request", views.password_reset_request,
         name="password_reset_request"),
    # path('useradd', views.useradd, name='useradd'),
    # path('userread', views.userread, name='userread'),
    # path('userdelete/<int:id>/', views.user_delete, name='userdelete'),
    # path('userupdate/<int:id>/', views.user_update, name='userupdate'),
    # path("changepass/", views.user_change_pass, name="changepass"),
]
