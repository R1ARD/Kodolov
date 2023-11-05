
from django.contrib import admin
from django.urls import path

from pages import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.AppointmentListView.as_view(), name='home'),
    path('about/', views.aboutPageView, name ='about'),
    path('Appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='Appointment_detail'),
    path('Appointment/new/', views.AppointmentCreateView.as_view(), name='Appointment_new'),
]
