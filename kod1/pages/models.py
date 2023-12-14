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

    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Medicine(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название лекарства', null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Лекарство"
        verbose_name_plural = "Лекарства"

class Disease(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название болезни', null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    medicines = models.OneToOneField(Medicine, related_name='diseases', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Болезнь"
        verbose_name_plural = "Болезни"




class Pet(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя питомца', null=True)
    species = models.CharField(max_length=50, verbose_name='Вид', null=True)
    breed = models.CharField(max_length=50, verbose_name='Порода', blank=True, null=True)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': False}, verbose_name='Владелец', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"

    def get_absolute_url(self):
        return reverse('pet_detail', args=[str(self.id)])



class Appointment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='Питомец', null=True)
    veterinarian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, verbose_name='Ветеринар', null=True, related_name='veterinarian_appointments')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': False}, verbose_name='Владелец питомца', null=True, related_name='owner_appointments')
    createDate = models.DateTimeField(verbose_name='Дата отправки заявки', auto_now_add=True, null=True)
    date = models.DateTimeField(verbose_name='Дата и время приема', null=True, unique=True)
    notes = models.TextField(verbose_name='Заметки', blank=True, null=True)
    is_processed = models.BooleanField(default=False, verbose_name='Заявка рассмотрена')

    def __str__(self):
        return f"{self.owner.first_name}'s {self.pet.name} -> {self.veterinarian.first_name} : {self.date}"

    def get_absolute_url(self):
        return reverse('appointment_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Заявление"
        verbose_name_plural = "Заявления"


class Diagnosis(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='Питомец', null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    disease = models.ForeignKey(Disease, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Название болезни')
    createDate = models.DateTimeField(verbose_name='Дата постановки', auto_now_add=True, null=True)
    veterinarian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Ветеринар', null=True, related_name='veterinarian_diagnoses')

    def get_absolute_url(self):
        return reverse('diagnosis_detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.pet.name} -> {self.disease.name}"

    class Meta:
        verbose_name = "Диагноз"
        verbose_name_plural = "Диагнозы"
