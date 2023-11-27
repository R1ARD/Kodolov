from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('appointment/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointment/<int:pk>/edit', views.AppointmentUpdateView.as_view(), name='appointment_edit'),
    path('appointment/<int:pk>/delete', views.AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointment/new/', views.AppointmentCreateView.as_view(), name='appointment_new'),
]