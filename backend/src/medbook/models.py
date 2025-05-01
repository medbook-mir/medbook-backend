from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    pass
    # username = None
    # email = models.EmailField(unique=True, verbose_name='Email')
    # phone_regex = RegexValidator(
    #     regex=r'^\+?1?\d{9,12}$',
    #     message="Номер телефона должен быть в формате: '+999999999'. До 12 цифр."
    # )
    # phone = models.CharField(
    #     validators=[phone_regex],
    #     max_length=17,
    #     blank=True,
    #     verbose_name='Телефон'
    # )
    # birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    
    # blood_type = models.CharField(
    #     max_length=3,
    #     blank=True,
    #     choices=[
    #         ('A+', 'A+'),
    #         ('A-', 'A-'),
    #         ('B+', 'B+'),
    #         ('B-', 'B-'),
    #         ('AB+', 'AB+'),
    #         ('AB-', 'AB-'),
    #         ('O+', 'O+'),
    #         ('O-', 'O-'),
    #     ],
    #     verbose_name='Группа крови'
    # )
    # allergies = models.TextField(blank=True, verbose_name='Аллергии')
    # chronic_diseases = models.TextField(blank=True, verbose_name='Хронические заболевания')
    
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = [] 

    # class Meta:
    #     verbose_name = 'Пользователь'
    #     verbose_name_plural = 'Пользователи'

    # def __str__(self):
    #     return self.email