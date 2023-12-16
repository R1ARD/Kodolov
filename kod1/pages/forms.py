from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Pet, Appointment
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import datetime


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'father_name', 'username', 'birth_date', 'gender', 'phone', 'email')
        widgets = {
            'birth_date': forms.DateTimeInput(attrs={'type':'date', 'required':'required'}, format='%Y-%m-%d'),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        # Проверка на то, что дата рождения не в будущем
        if birth_date > timezone.now().date():
            raise ValidationError("Дата рождения не может быть в будущем.")

        # Проверка на совершеннолетие (18 лет)
        age = timezone.now().date() - birth_date
        if age < timedelta(days=18 * 365.25):  # Учитываем високосные годы
            raise ValidationError("Необходимо быть совершеннолетним (18 лет).")

        return birth_date


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'father_name', 'username', 'birth_date', 'gender', 'phone', 'email')
        widgets = {
            'birth_date': forms.DateTimeInput(attrs={'type': 'date', 'required': 'required'}, format='%Y-%m-%d')
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        # Проверка на то, что дата рождения не в будущем
        if birth_date > timezone.now().date():
            raise ValidationError("Дата рождения не может быть в будущем.")

        # Проверка на совершеннолетие (18 лет)
        age = timezone.now().date() - birth_date
        if age < timedelta(days=18 * 365.25):  # Учитываем високосные годы
            raise ValidationError("Необходимо быть совершеннолетним (18 лет).")

        return birth_date


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ('name', 'species', 'breed', 'birth_date')
        widgets = {
            'birth_date': forms.DateTimeInput(attrs={'type': 'date', 'required': 'required'}, format='%Y-%m-%d')
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        # Проверка на то, что дата рождения не в будущем
        if birth_date > timezone.now().date():
            raise ValidationError("Дата рождения не может быть в будущем.")
        return birth_date

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('pet', 'services', 'veterinarian', 'date', 'notes')
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': 'required', 'step': 1800}, format='%Y-%m-%d %H:%M' )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Настройка начального и конечного времени для выбора
        now = timezone.localtime()

        # Получение уже занятых временных слотов
        existing_appointments = Appointment.objects.filter(
            date__date=now.date(),
            date__gte=now
        ).values_list('date', flat=True)

        # Фильтруйте занятые временные слоты
        self.exclude_times = existing_appointments

    def clean_date(self):
        date = self.cleaned_data.get('date')

        if date.time() < datetime.time(8, 0) or date.time() > datetime.time(21, 0):
            raise forms.ValidationError("Выбранное время вне рабочих часов.")

        if date in self.exclude_times:
            raise forms.ValidationError("Это время уже занято.")

        # Проверка на то, что дата рождения не в прошлом
        if date < timezone.now():
            raise ValidationError("Дата записи не может быть в прошлом.")

        if date.minute not in [0, 30]:
            raise ValidationError("Время должно быть выбрано с шагом в 30 минут.")

        return date

