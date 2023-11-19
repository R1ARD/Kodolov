from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import OwnerCreationForm, OwnerChangeForm
from .models import Owner

from django.contrib import admin
from .models import Veterinarian
from .models import Appointment
from .models import Medicine
from .models import Disease

from .models import Pet

# Register your models here.
class OwnerAdmin(UserAdmin):
    add_form = OwnerCreationForm
    form = OwnerChangeForm
    list_display = ['first_name','last_name', 'father_name', 'username', 'birth_date', 'gender', 'phone', 'email']
    model = Owner

admin.site.register(Owner, OwnerAdmin)