from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#from .forms import OwnerCreationForm, OwnerChangeForm


from django.contrib import admin
from .models import Veterinarian
from .models import Appointment
from .models import Medicine
from .models import Disease
from .models import Owner
from .models import Pet

# Register your models here.



admin.site.register(Owner)
admin.site.register(Appointment)
admin.site.register(Pet)
admin.site.register(Disease)
admin.site.register(Medicine)
admin.site.register(Veterinarian)