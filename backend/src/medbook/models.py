import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class BaseTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseTimeStampModel):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
        ("prefer_not_to_say", "Prefer not to say"),
    ]

    class Role(models.TextChoices):
        SUPERADMIN = "SUPERADMIN", "Superadmin"
        ADMIN = "ADMIN", "Admin"
        DOCTOR = "DOCTOR", "Doctor"
        PATIENT = "PATIENT", "Patinet"
        CLINIC = "CLINIC", "Clinic"

    base_role = Role.SUPERADMIN
    role = models.CharField(
        max_length=50, choices=Role.choices, db_index=True, null=True, blank=True
    )
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email_code = models.CharField(max_length=6, null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES, blank=True, null=True
    )
    profile_image_url = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        if not self.email and not self.phone_number and not self.username:
            raise ValidationError("Either email or phone number must be provided")

    def save(self, *args, **kwargs):
        if not self.pk and not self.role:
            self.role = self.base_role

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


class Specialty(BaseTimeStampModel):
    CATEGORY_CHOICES = [
        ("primary_care", "Primary Care"),
        ("specialist", "Specialist"),
        ("surgery", "Surgery"),
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Clinic(BaseTimeStampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    website_url = models.URLField(blank=True, null=True)
    profile_image_url = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    established_year = models.IntegerField(blank=True, null=True)
    total_staff = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_clinics",
    )
    is_deleted = models.DateTimeField(blank=True, null=True)
    base_role = User.Role.CLINIC

    def save(self, *args, **kwargs):
        if self.user_id:
            self.user.role = self.base_role
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Doctor(BaseTimeStampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, blank=True, null=True)
    license_number = models.CharField(
        max_length=100, unique=True, blank=True, null=True
    )
    consultation_fee = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    online_consultation_fee = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    average_consultation_time = models.IntegerField(
        blank=True, null=True, help_text="in minutes"
    )
    is_online_consultation_available = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    total_patients = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    specialty = models.ForeignKey(
        Specialty, on_delete=models.CASCADE, blank=True, null=True
    )
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="verified_doctors",
    )
    is_deleted = models.DateTimeField(blank=True, null=True)
    base_role = User.Role.DOCTOR

    def save(self, *args, **kwargs):
        if self.user_id:
            self.user.role = self.base_role
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.license_number})"


class Patient(BaseTimeStampModel):
    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(blank=True, null=True)
    blood_group = models.CharField(
        max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True
    )
    medical_allergies = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    insurance_provider = models.CharField(max_length=255, blank=True, null=True)
    insurance_number = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.DateTimeField(blank=True, null=True)
    base_role = User.Role.PATIENT

    def save(self, *args, **kwargs):
        if self.user_id:
            self.user.role = self.base_role
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Patient: {self.user.first_name} {self.user.last_name}"


class MedicalTest(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
