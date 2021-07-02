from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('', views.productadd, name='productadd'),
    path('productread', views.productread, name='productread'),
    path('productdelete/<int:id>/', views.product_delete, name='productdelete'),
    path('productupdate/<int:id>/', views.product_update, name='productupdate'),

]
