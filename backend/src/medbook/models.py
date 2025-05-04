from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class MedicalTest(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name