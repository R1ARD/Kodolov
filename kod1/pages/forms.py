from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Owner


class OwnerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Owner
        fields = ('first_name','last_name', 'father_name',  'birth_date', 'gender', 'phone', 'email')


class OwnerChangeForm(UserChangeForm):
    class Meta:
        model = Owner
        fields = ('first_name','last_name', 'father_name', 'username', 'birth_date', 'gender', 'phone', 'email')
