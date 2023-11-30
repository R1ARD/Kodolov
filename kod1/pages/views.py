from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .forms import CustomUserCreationForm, AppointmentForm
from . import models
# Create your views here.
from django.http import HttpResponse

def homePageView(request):
    return render(request, "home.html")

def aboutPageView(request):
    return render(request, "about.html")

class SignUp(CreateView):
    form_class = CustomUserCreationForm
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


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_staff:
            raise PermissionDenied
        return True

#Appointment
class AppointmentListView(LoginRequiredMixin, ListView):
    model = models.Appointment
    template_name = 'appointment_list.html'
    login_url = 'login'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(owner__first_name__icontains=query)
        return queryset

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = models.Appointment
    template_name = 'appointment_detail.html'
    login_url = 'login'

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = models.Appointment
    template_name = 'appointment_new.html'
    #fields = ['pet', 'veterinarian', 'date', 'notes']
    login_url = 'login'
    form_class = AppointmentForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['pet'].queryset = models.Pet.objects.filter(owner=self.request.user)
        return form

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

#Pet

class PetListView(LoginRequiredMixin, IsOwnerOrAdminMixin, ListView):
    model = models.Pet
    template_name = 'appointment_list.html'
    login_url = 'login'

class PetDetailView(LoginRequiredMixin, IsOwnerOrAdminMixin, DetailView):
    model = models.Pet
    template_name = 'appointment_detail.html'
    login_url = 'login'

class PetCreateView(LoginRequiredMixin, IsAdminMixin, CreateView):
    model = models.Pet
    template_name = 'appointment_new.html'
    fields = "__all__"
    login_url = 'login'
    form_class = AppointmentForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['pet'].queryset = models.Pet.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PetUpdateView(LoginRequiredMixin, IsAdminMixin, UpdateView):
    model = models.Pet
    fields = ['date', 'veterinarian', 'pet']
    template_name = 'appointment_edit.html'
    login_url = 'login'

class PetDeleteView(LoginRequiredMixin, IsAdminMixin, DeleteView):
    model = models.Pet
    template_name = 'appointment_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

