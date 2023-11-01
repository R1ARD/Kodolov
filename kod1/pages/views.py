from django.shortcuts import render
from django.views.generic import ListView
from .models import Appointment
# Create your views here.
from django.http import HttpResponse

def homePageView(request):
    return render(request, "home.html")

def aboutPageView(request):
    return render(request, "about.html")

class AppointmentListView(ListView):
    model = Appointment
    template_name = 'home.html'
