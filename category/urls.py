from django.urls import path
from . import views


app_name = 'category'
urlpatterns = [
    path('', views.Categoryadd, name='categoryadd'),
    path('categoryread', views.categoryread, name='categoryread'),
    path('categorydelete/<int:id>/', views.category_delete, name='categorydelete'),
    path('categoryupdate/<int:id>/', views.category_update, name='categoryupdate'),
]
