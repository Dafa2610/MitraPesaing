from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.GetFirebaseDataCronJob)
    # url untuk menentukan pengiriman data
]