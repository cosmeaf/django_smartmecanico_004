from django.urls import path
from django.contrib import admin
from . import views

app_name = 'app_address'

urlpatterns = [
    path('add/', views.AddressAddView.as_view(), name='address_add'),
    # rest of the URLs
]
