from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Appointment
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import OwnerCreationForm
# Create your views here.
from django.http import HttpResponse

def homePageView(request):
    return render(request, "home.html")

def aboutPageView(request):
    return render(request, "about.html")

class SignUp(CreateView):
    form_class = OwnerCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class AppointmentListView(ListView):
    model = Appointment
    template_name = 'home.html'

class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = 'appointment_detail.html'

class AppointmentCreateView(CreateView):
    model = Appointment
    template_name = 'appointment_new.html'
    fields = '__all__'

class AppointmentUpdateView(UpdateView):
    model = Appointment
    fields = ['date', 'veterinarian', 'pet']
    template_name = 'appointment_edit.html'

class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = 'appointment_delete.html'
    success_url = reverse_lazy('home')

