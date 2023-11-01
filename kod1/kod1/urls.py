
from django.contrib import admin
from django.urls import path

from pages import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.AppointmentListView.as_view(), name='home'),
    path('about/', views.aboutPageView, name ='about'),
]
