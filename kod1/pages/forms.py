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
        fields = ('first_name', 'last_name', 'father_name', 'username', 'phone', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'father_name', 'username', 'phone', 'email')

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
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': 'required', 'step': 1800}, format='%Y-%m-%d %H:%M')
        }

    def clean(self):
        cleaned_data = super().clean()

        # Получение уже занятых временных слотов только для данного ветеринара
        now = timezone.localtime()

        start_time = datetime.time(8, 0)
        existing_appointments = Appointment.objects.filter(
            date__date=now.date(),
            date__gte=now,
            veterinarian=cleaned_data.get('veterinarian')
        ).values_list('date', flat=True)

        # Фильтруйте занятые временные слоты
        exclude_times = existing_appointments

        date = cleaned_data.get('date')
        if date:
            if date.time() < datetime.time(8, 0) or date.time() > datetime.time(21, 0):
                self.add_error('date', "Выбранное время вне рабочих часов.")

            if date in exclude_times:
                self.add_error('date', "Это время уже занято.")

            # Проверка на то, что дата записи не в прошлом
            if date < timezone.now():
                self.add_error('date', "Дата записи не может быть в прошлом.")

            if date.minute not in [0, 30]:
                self.add_error('date', "Время должно быть выбрано с шагом в 30 минут.")

