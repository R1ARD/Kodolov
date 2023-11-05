from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Appointment
from django.views.generic.edit import CreateView
# Create your views here.
from django.http import HttpResponse

def homePageView(request):
    return render(request, "home.html")

def aboutPageView(request):
    return render(request, "about.html")

class AppointmentListView(ListView):
    model = Appointment
    template_name = 'home.html'

class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = 'Appointment_detail.html'

class AppointmentCreateView(CreateView):
    model = Appointment
    template_name = 'Appointment_new.html'
    fields = '__all__'