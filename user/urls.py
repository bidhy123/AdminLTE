from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('ji', views.useradd, name='useradd'),
    path('userread', views.userread, name='userread'),
    path('userdelete/<int:id>/', views.user_delete, name='userdelete'),
    path('userupdate/<int:id>/', views.user_update, name='userupdate'),
]
