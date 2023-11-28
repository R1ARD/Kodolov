from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', null=True)
    father_name = models.CharField(max_length=50, verbose_name='Отчество', blank=True, null=True)
    gender = models.CharField(max_length=50, verbose_name='Гендер', null=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class VeterinarianProfile(models.Model):
    specialization = models.CharField(max_length=50, verbose_name='Специализация', null=True)
    education = models.CharField(max_length=50, verbose_name='Образование', null=True)
    veterinarian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, verbose_name='Ветеринар', null=True)

class Pet(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя питомца', null=True)
    species = models.CharField(max_length=50, verbose_name='Вид', null=True)
    breed = models.CharField(max_length=50, verbose_name='Порода', blank=True, null=True)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': False}, verbose_name='Владелец', null=True)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название лекарства', null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название болезни', null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    medicines = models.OneToOneField(Medicine, related_name='diseases', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='Питомец', null=True)
    veterinarian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, verbose_name='Ветеринар', null=True, related_name='veterinarian_appointments')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': False}, verbose_name='Владелец питомца', null=True, related_name='owner_appointments')
    createDate = models.DateTimeField(verbose_name='Дата отправки заявки', auto_now_add=True, null=True)
    date = models.DateTimeField(verbose_name='Дата и время приема', null=True)
    notes = models.TextField(verbose_name='Заметки', blank=True, null=True)

    def __str__(self):
        return f"{self.owner.first_name}'s {self.pet.name} -> {self.veterinarian.first_name} : {self.date}"

    def get_absolute_url(self):
        return reverse('appointment_detail', args=[str(self.id)])
