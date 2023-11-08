
from django.contrib import admin
from django.urls import path

from pages import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.AppointmentListView.as_view(), name='home'),
    path('about/', views.aboutPageView, name='about'),
    path('appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointment/new/', views.AppointmentCreateView.as_view(), name='appointment_new'),
    path('appointment/<int:pk>/delete', views.AppointmentDeleteView.as_view(), name='appointment_delete'),
]
