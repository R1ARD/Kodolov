from django.contrib import admin

from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Service)
admin.site.register(models.Disease)
admin.site.register(models.Medicine)
admin.site.register(models.CustomUser)


