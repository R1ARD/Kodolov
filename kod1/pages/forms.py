from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Pet
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


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
        fields = "__all__"
        widgets = {
            'birth_date': forms.DateTimeInput(attrs={'type': 'date', 'required': 'required'}, format='%Y-%m-%d')
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        # Проверка на то, что дата рождения не в будущем
        if birth_date > timezone.now().date():
            raise ValidationError("Дата рождения не может быть в будущем.")
        return birth_date
