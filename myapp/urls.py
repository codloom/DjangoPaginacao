from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.product_list, name='product-list'), 
]