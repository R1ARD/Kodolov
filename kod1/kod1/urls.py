
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from pages import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.AppointmentListView.as_view(), name='home'),
    path('about/', views.aboutPageView, name='about'),
    path('appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointment/new/', views.AppointmentCreateView.as_view(), name='appointment_new'),
    path('appointment/<int:pk>/edit', views.AppointmentUpdateView.as_view(), name='appointment_edit'),
    path('appointment/<int:pk>/delete', views.AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('pages/', include('pages.urls')),
    path('pages/', include('django.contrib.auth.urls')),

]
