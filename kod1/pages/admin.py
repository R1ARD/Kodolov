from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm


from django.contrib import admin
from .models import Appointment
from .models import Medicine
from .models import Disease
from .models import CustomUser
from .models import Pet

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['first_name', 'last_name', 'father_name', 'username', 'birth_date', 'gender', 'phone', 'email']
    if(CustomUser.is_staff == True):
        list_display.append('specialization')
        list_display.append('education')
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Appointment)
admin.site.register(Pet)
admin.site.register(Disease)
admin.site.register(Medicine)

