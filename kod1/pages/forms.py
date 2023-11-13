from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Owner


class OwnerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Owner
        fields = UserCreationForm.Meta.fields


class OwnerChangeForm(UserChangeForm):
    class Meta:
        model = Owner
        fields = UserChangeForm.Meta.fields
