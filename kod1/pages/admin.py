from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm


from django.contrib import admin
from . import models


# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['first_name', 'last_name', 'father_name', 'username', 'birth_date', 'gender', 'phone', 'email']


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Appointment)
admin.site.register(models.Pet)
admin.site.register(models.Disease)
admin.site.register(models.Medicine)
admin.site.register(models.Diagnosis)

