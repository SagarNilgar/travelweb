from django.contrib import admin
from django.urls import path, include
from  calc import views
urlpatterns = [
    path('',views.home, name='home'),
    path('add',views.add, name='add'),
    
]
