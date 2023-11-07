from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.get_data_from_firebase)
    # url untuk menentukan pengiriman data
]