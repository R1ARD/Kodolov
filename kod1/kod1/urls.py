
from django.contrib import admin
from django.urls import path

from pages import views

urlpatterns = [
    path('about/', views.aboutView),
    path('', views.index),
]
