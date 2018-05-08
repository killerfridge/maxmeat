from . import views
from django.urls import path


app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('products/', views.product_list, name='product_list'),
    path('products/<str:category_slug>/', views.product_list, name='product_list_by_category'),
    path('products/<int:id>/<str:slug>/', views.product_detail, name='product_detail'),
]