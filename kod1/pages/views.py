from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Sum, Exists, OuterRef
from django.contrib.auth import get_user_model
from datetime import timedelta, date
from django.views import View

from .forms import CustomUserCreationForm, CustomUserChangeForm, PetForm, AppointmentForm
from . import models
# Create your views here.
from django.http import HttpResponse

def homePageView(request):
    return render(request, "home.html")

def get_statistics(request):
    today = date.today()
    month_ago = today - timedelta(days=30)
    quarter_ago = today - timedelta(days=90)
    year_ago = today - timedelta(days=365)

    # Функция для подсчета статистики за определенный период
    def calculate_stats(start_date):
        return models.Appointment.objects.filter(
            is_processed=True,
            date__gte=start_date,
            date__lte=today
        ).aggregate(
            total=Sum('services__price')
        )['total'] or 0  # Возвращаем 0, если нет данных

    month_total = calculate_stats(month_ago)
    quarter_total = calculate_stats(quarter_ago)
    year_total = calculate_stats(year_ago)

    context = {
        'month_total': month_total,
        'quarter_total': quarter_total,
        'year_total': year_total
    }
    return render(request, 'statistics.html', context)


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

class IsNotStaffMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_staff:
            raise PermissionDenied
        return True



class UserIsUserMixin(UserPassesTestMixin):
    def test_func(self):
        user = get_object_or_404(get_user_model(), pk=self.kwargs.get('pk'))
        return self.request.user == user

    def handle_no_permission(self):
        raise PermissionDenied

#Appointment


class AppointmentListView(LoginRequiredMixin, ListView):
    model = models.Appointment
    template_name = 'appointment_list.html'
    login_url = 'login'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Проверяем, является ли пользователь ветеринаром (пример: по атрибуту is_staff)
        if self.request.user.is_staff:
            queryset = queryset.filter(veterinarian=self.request.user, is_processed=False)
        else:
            queryset = queryset.filter(owner=self.request.user, is_processed=False)

        queryset = queryset.annotate(total_price=Sum('services__price'))

        query = self.request.GET.get('appointment-search')
        if query:
            if self.request.user.is_staff:
                queryset = queryset.filter(Q(owner__first_name__icontains=query) |
                                           Q(owner__last_name__icontains=query) |
                                           Q(owner__username__icontains=query) |
                                           Q(pet__name__icontains=query))
            else:
                queryset = queryset.filter(Q(veterinarian__first_name__icontains=query) |
                                           Q(veterinarian__last_name__icontains=query) |
                                           Q(veterinarian__username__icontains=query) |
                                           Q(pet__name__icontains=query))
        return queryset

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = models.Appointment
    template_name = 'appointment_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = self.get_object()

        # Расчет общей стоимости услуг
        total_price = appointment.services.aggregate(Sum('price'))['price__sum']

        # Добавление суммы цен в контекст
        context['total_price'] = total_price if total_price else 0
        return context


class AppointmentCreateView(LoginRequiredMixin, IsNotStaffMixin, CreateView):
    model = models.Appointment
    template_name = 'appointment_new.html'
    form_class = AppointmentForm
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
    form_class = AppointmentForm
    template_name = 'conclusion_edit.html'
    login_url = 'login'


def AppointmentProcess(request, pk):
    appointment = get_object_or_404(models.Appointment, pk=pk)

    # Проверяем, имеет ли пользователь право изменить эту запись
    if appointment.veterinarian == request.user or request.user.is_staff:
        appointment.is_processed = True
        appointment.save()

    return redirect('appointment_list')  # Название вашего URL для AppointmentListView

# class AppointmentDeleteView(LoginRequiredMixin, IsOwnerOrAdminMixin, DeleteView):
#     model = models.Appointment
#     template_name = 'appointment_delete.html'
#     success_url = reverse_lazy('home')
#     login_url = 'login'

#Pet



class PetListView(LoginRequiredMixin, ListView):
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

class PetCreateView(LoginRequiredMixin, CreateView):
    model = models.Pet
    template_name = 'pet_new.html'
    form_class = PetForm
    login_url = 'login'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)



class PetUpdateView(LoginRequiredMixin, IsNotStaffMixin, UpdateView):
    model = models.Pet
    template_name = 'pet_edit.html'
    form_class = PetForm
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

#Conclusion

class ConclusionCreateView(LoginRequiredMixin, IsAdminMixin, CreateView):
    model = models.Conclusion
    fields = ['description']
    template_name = 'conclusion_new.html'

    def form_valid(self, form):
        # Получение записи на прием и установка питомца с ветеринаром
        appointment = get_object_or_404(models.Appointment, pk=self.kwargs['appointment_id'])
        form.instance.pet = appointment.pet
        form.instance.veterinarian = appointment.veterinarian
        # Обновление записи на прием как обработанной
        appointment.is_processed = True
        appointment.save()
        return super().form_valid(form)

class ConclusionDetailView(LoginRequiredMixin, DetailView):
    model = models.Conclusion
    template_name = 'conclusion_detail.html'
    login_url = 'login'

class ConclusionUpdateView(LoginRequiredMixin, UserIsUserMixin, UpdateView):
    model = models.Conclusion
    fields = ['description']
    template_name = 'conclusion_edit.html'
    login_url = 'login'

class ConclusionListView(ListView):
    model = models.Conclusion
    template_name = 'conclusion_list.html'  # укажите путь к вашему шаблону

    def get_queryset(self):
        """
        Переопределение queryset для фильтрации диагнозов по питомцу.
        """
        pet_id = self.kwargs.get('pet_id')
        return models.Conclusion.objects.filter(pet__id=pet_id)

#Service

class ServiceListView(ListView):
    model = models.Service
    template_name = 'home.html'