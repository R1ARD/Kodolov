from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', null=True)
    father_name = models.CharField(max_length=50, verbose_name='Отчество', blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True)
    specialization = models.CharField(max_length=50, verbose_name='Специализация', blank=True, null=True)

    def __str__(self):
        return f"{self.last_name}  {self.first_name}"

    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"




class Pet(models.Model):
    name = models.CharField(max_length=50, verbose_name='Кличка питомца', null=True)
    species = models.CharField(max_length=50, verbose_name='Вид', null=True)
    breed = models.CharField(max_length=50, verbose_name='Порода', blank=True, null=True)
    birth_date = models.DateField(verbose_name='Дата рождения', null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': False}, verbose_name='Владелец', null=True)
    care_requirements = models.TextField(verbose_name='Требования к уходу', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"

    def get_absolute_url(self):
        return reverse('pet_detail', args=[str(self.id)])

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название услуги')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f"{self.name} - {self.price} руб."

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

class Appointment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='Питомец', null=True)
    veterinarian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, verbose_name='Ветеринар', null=True, related_name='veterinarian_appointments')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': False}, verbose_name='Владелец питомца', null=True, related_name='owner_appointments')
    create_date = models.DateTimeField(verbose_name='Дата отправки заявки', auto_now_add=True, null=True)
    date = models.DateTimeField(verbose_name='Дата и время приема', null=True)
    notes = models.TextField(verbose_name='Дополнительная информация', blank=True, null=True)
    is_processed = models.BooleanField(default=False, verbose_name='Заявка рассмотрена')
    services = models.ManyToManyField(Service, verbose_name='Услуги')



    def __str__(self):
        return f"{self.owner.first_name}'s {self.pet.name} -> {self.veterinarian.first_name} : {self.date}"

    def get_absolute_url(self):
        return reverse('appointment_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Заявление"
        verbose_name_plural = "Заявления"


class Conclusion(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='Питомец', null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    create_date = models.DateTimeField(verbose_name='Дата постановки', auto_now_add=True, null=True)
    veterinarian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Ветеринар', null=True, related_name='veterinarian_diagnoses')

    def get_absolute_url(self):
        return reverse('сonclusion_detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.create_date} - {self.veterinarian} - {self.pet.name}"

    class Meta:
        verbose_name = "Заключение"
        verbose_name_plural = "Заключения"
