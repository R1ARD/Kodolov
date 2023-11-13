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
    list_display = ['username', 'birth_date', 'email']
    model = Owner

admin.site.register(Owner, OwnerAdmin)