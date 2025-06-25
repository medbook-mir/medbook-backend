import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email_code = models.CharField(max_length=4, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_gender = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        if not self.email and not self.phone_number and not self.username:
            raise ValidationError("Either email or phone number must be provided")

    def save(self, *args, **kwargs):
        if self.username:
            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if re.match(email_pattern, self.username):
                self.email = self.username
                self.phone_number = None
            else:
                self.phone_number = self.username
                self.email = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.username}"


class MedicalTest(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
