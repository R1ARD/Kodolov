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
    path('appointment/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointment/<int:pk>/edit', views.AppointmentUpdateView.as_view(), name='appointment_edit'),
    path('appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointment/new/', views.AppointmentCreateView.as_view(), name='appointment_new'),
    path('appointment/process/<int:pk>/', views.AppointmentProcess, name='appointment_process'),
    #Pet
    path('pet/', views.PetListView.as_view(), name='pet_list'),
    path('pet/<int:pk>/edit', views.PetUpdateView.as_view(), name='pet_edit'),
    path('pet/<int:pk>/', views.PetDetailView.as_view(), name='pet_detail'),
    path('pet/new/', views.PetCreateView.as_view(), name='pet_new'),
    #Conclusio
    path('pet/conclusions/<int:pet_id>/', views.ConclusionListView.as_view(), name='conclusion_list'),
    path('conclusion/create/<int:appointment_id>/', views.ConclusionCreateView.as_view(), name='conclusion_new'),
    path('conclusion/<int:pk>/', views.ConclusionDetailView.as_view(), name='conclusion_detail'),
    path('conclusion/<int:pk>/edit', views.ConclusionUpdateView.as_view(), name='conclusion_edit'),
]
