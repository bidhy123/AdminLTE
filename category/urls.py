from django.urls import path
from . import views


app_name = 'category'
urlpatterns = [
    path('', views.categoryadd, name='categoryadd'),
    path('', views.categoryread, name='categoryread'),
]
