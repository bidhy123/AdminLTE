from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.useradd, name='useradd'),
    path('userread', views.userread, name='userread'),
]
