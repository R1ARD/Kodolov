from django.contrib import admin

from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Service)
admin.site.register(models.CustomUser)
admin.site.register(models.Pet)
admin.site.register(models.Appointment)
