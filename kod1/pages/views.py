from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm, CustomUserChangeForm, PetForm
from . import models
# Create your views here.
from django.http import HttpResponse

def homePageView(request):
    return render(request, "home.html")


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


class UserIsUserMixin(UserPassesTestMixin):
    def test_func(self):
        user = get_object_or_404(get_user_model(), pk=self.kwargs.get('pk'))
        return self.request.user == user

    def handle_no_permission(self):
        raise PermissionDenied

#Appointment


class VetAppointmentListView(LoginRequiredMixin, IsAdminMixin,ListView):
    model = models.Appointment
    template_name = 'appointment_list.html'
    login_url = 'login'

    def get_queryset(self):
        queryset = super().get_queryset().filter(veterinarian=self.request.user, is_processed=False)
        query = self.request.GET.get('appointment-search')
        if query:
            queryset = queryset.filter(Q(owner__first_name__icontains=query) |
                                       Q(owner__last_name__icontains=query) |
                                       Q(owner__username__icontains=query) |
                                       Q(veterinarian__first_name__icontains=query) |
                                       Q(veterinarian__last_name__icontains=query) |
                                       Q(veterinarian__username__icontains=query) |
                                       Q(pet__name__icontains=query))
        return queryset


class UsersAppointmentListView(LoginRequiredMixin, ListView):
    model = models.Appointment
    template_name = 'appointment_list.html'
    login_url = 'login'

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)
        query = self.request.GET.get('appointment-search')
        if query:
            queryset = queryset.filter(Q(veterinarian__first_name__icontains=query) |
                                       Q(veterinarian__last_name__icontains=query) |
                                       Q(veterinarian__username__icontains=query) |
                                       Q(pet__name__icontains=query))
        return queryset


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = models.Appointment
    template_name = 'appointment_detail.html'
    login_url = 'login'


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = models.Appointment
    template_name = 'appointment_new.html'
    fields = ['pet', 'veterinarian', 'date', 'notes']
    login_url = 'login'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['pet'].queryset = models.Pet.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, IsOwnerOrAdminMixin, UpdateView):
    model = models.Appointment
    fields = ['pet', 'veterinarian', 'date', 'notes']
    template_name = 'diagnosis_edit.html'
    login_url = 'login'


class AppointmentDeleteView(LoginRequiredMixin, IsOwnerOrAdminMixin, DeleteView):
    model = models.Appointment
    template_name = 'appointment_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

#Pet


class PetListView(LoginRequiredMixin, IsAdminMixin, ListView):
    model = models.Pet
    template_name = 'pet_list.html'
    login_url = 'login'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query))
        return queryset

class UsersPetListView(LoginRequiredMixin, ListView):
    model = models.Pet
    template_name = 'pet_list.html'
    login_url = 'login'

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)
        query = self.request.GET.get('pet-search')
        if query:
            queryset = queryset.filter(Q(name__icontains=query))
        return queryset


class PetDetailView(LoginRequiredMixin, IsOwnerOrAdminMixin, DetailView):
    model = models.Pet
    template_name = 'pet_detail.html'
    login_url = 'login'

class PetCreateView(LoginRequiredMixin, IsAdminMixin, CreateView):
    model = models.Pet
    template_name = 'pet_new.html'
    form_class = PetForm
    login_url = 'login'



class PetUpdateView(LoginRequiredMixin, IsAdminMixin, UpdateView):
    model = models.Pet
    template_name = 'pet_edit.html'
    form_class = PetForm
    login_url = 'login'

class PetDeleteView(LoginRequiredMixin, IsAdminMixin, DeleteView):
    model = models.Pet
    template_name = 'pet_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

#User

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = models.CustomUser
    template_name = 'user_detail.html'
    login_url = 'login'

class UserUpdateView(LoginRequiredMixin, UserIsUserMixin, UpdateView):
    model = models.CustomUser
    form_class = CustomUserChangeForm
    template_name = 'user_edit.html'
    login_url = 'login'

#Diagnosis

class DiagnosisCreateView(LoginRequiredMixin, IsAdminMixin, CreateView):
    model = models.Diagnosis
    fields = [ 'disease', 'description']
    template_name = 'diagnosis_new.html'

    def form_valid(self, form):
        # Получение записи на прием и установка питомца с ветеринаром
        appointment = get_object_or_404(models.Appointment, pk=self.kwargs['appointment_id'])
        form.instance.pet = appointment.pet
        form.instance.veterinarian = appointment.veterinarian
        # Обновление записи на прием как обработанной
        appointment.is_processed = True
        appointment.save()
        return super().form_valid(form)

class DiagnosisDetailView(LoginRequiredMixin, DetailView):
    model = models.Diagnosis
    template_name = 'diagnosis_detail.html'
    login_url = 'login'

class DiagnosisUpdateView(LoginRequiredMixin, UserIsUserMixin, UpdateView):
    model = models.Diagnosis
    fields = ['disease', 'description']
    template_name = 'diagnosis_edit.html'
    login_url = 'login'
