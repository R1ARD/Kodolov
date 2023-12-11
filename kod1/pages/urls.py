from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/edit', views.UserUpdateView.as_view(), name='user_edit'),
    #Appointment
    path('appointment/', views.UsersAppointmentListView.as_view(), name='users_appointment_list'),
    path('veterinarian/appointment/', views.VetAppointmentListView.as_view(), name='vet_appointment_list'),
    path('appointment/<int:pk>/edit', views.AppointmentUpdateView.as_view(), name='appointment_edit'),
    path('appointment/<int:pk>/delete', views.AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointment/new/', views.AppointmentCreateView.as_view(), name='appointment_new'),
    #Pet
    path('pet/', views.UsersPetListView.as_view(), name='users_pet_list'),
    path('pet/<int:pk>/edit', views.PetUpdateView.as_view(), name='pet_edit'),
    path('pet/<int:pk>/delete', views.PetDeleteView.as_view(), name='pet_delete'),
    path('pet/<int:pk>/', views.PetDetailView.as_view(), name='pet_detail'),
    path('pet/new/', views.PetCreateView.as_view(), name='pet_new'),
    #Diagnosis
    path('pet/diagnoses/<int:pet_id>/', views.DiagnosisListView.as_view(), name='diagnosis_list'),
    path('diagnosis/create/<int:appointment_id>/', views.DiagnosisCreateView.as_view(), name='diagnosis_new'),
    path('diagnosis/<int:pk>/', views.DiagnosisDetailView.as_view(), name='diagnosis_detail'),
    path('diagnosis/<int:pk>/edit', views.DiagnosisUpdateView.as_view(), name='diagnosis_edit'),
]