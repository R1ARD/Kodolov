from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .forms import OwnerCreationForm
from . import models
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

class IsOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        if user.is_staff or obj.owner == user:
            return True
        else:
            raise PermissionDenied


class AppointmentListView(LoginRequiredMixin, ListView):
    model = models.Appointment
    template_name = 'appointment_list.html'
    login_url = 'login'

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = models.Appointment
    template_name = 'appointment_detail.html'
    login_url = 'login'

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = models.Appointment
    template_name = 'appointment_new.html'
    fields = ['pet', 'veterinarian', 'date', 'notes']
    login_url = 'login'
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, IsOwnerOrAdminMixin, UpdateView):
    model = models.Appointment
    fields = ['date', 'veterinarian', 'pet']
    template_name = 'appointment_edit.html'
    login_url = 'login'

class AppointmentDeleteView(LoginRequiredMixin, IsOwnerOrAdminMixin, DeleteView):
    model = models.Appointment
    template_name = 'appointment_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'
