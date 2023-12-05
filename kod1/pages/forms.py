from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'father_name', 'username', 'birth_date', 'gender', 'phone', 'email')
        widgets = {
            'birth_date': forms.DateTimeInput(attrs={'type':'date', 'required':'required'}, format='%Y-%m-%d'),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'father_name', 'username', 'birth_date', 'gender', 'phone', 'email')
        widgets = {
            'birth_date': forms.DateTimeInput(attrs={'type': 'date', 'required': 'required'}, format='%Y-%m-%d')
        }


class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])