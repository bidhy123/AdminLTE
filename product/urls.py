from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('', views.productadd, name='productadd'),
    path('', views.productread, name='productread'),
]
