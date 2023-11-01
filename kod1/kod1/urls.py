
from django.contrib import admin
from django.urls import path

from pages import views

urlpatterns = [
    path('', views.homePageView, name='home'),
    path('about/', views.aboutPageView, name ='about'),
    path('admin/', admin.site.urls, name ='admin'),

]
