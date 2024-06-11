from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Pet, Appointment
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, time



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'father_name', 'username', 'phone', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'father_name', 'username', 'phone', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Удалить поле с паролем из формы
        del self.fields['password']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ('name', 'species', 'breed', 'birth_date', 'care_requirements')
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
        fields = ('pet', 'services', 'veterinarian', 'date', 'time', 'notes')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'required': 'required', 'min': date.today().isoformat()}),
            'time': forms.Select(choices=[(time(hour=x), f"{x}:00") for x in range(8, 22)], attrs={'required': 'required'}),
            'services': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AppointmentForm, self).__init__(*args, **kwargs)

        if user and user.is_superuser:
            # Убираем поле 'pet' для суперпользователя
            self.fields.pop('pet')