import os
import random
import re
import string

from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.mail import send_mail
from django.core.validators import FileExtensionValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from twilio.rest import Client


class AbstractBaseTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class AbstractBaseAddress(AbstractBaseTimeStampModel):
    address_line_1 = models.CharField(max_length=255, null=False)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=False)
    state = models.CharField(max_length=255, null=False)
    postal_code = models.CharField(max_length=255, null=False)
    country = models.CharField(max_length=255, null=False)
    is_main_address = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ImageUploadMixin:
    @staticmethod
    def get_upload_path(instance, filename):
        model_name = instance.__class__.__name__.lower()
        cleaned_model_name = model_name.replace('image', '')
        date_path = datetime.now().strftime('%Y/%m/%d')
        return f"{cleaned_model_name}_images/{date_path}/{filename}"


class AbstractBaseImage(AbstractBaseTimeStampModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        PENDING = "pending", "Pending"

    image = models.ImageField(
        upload_to=ImageUploadMixin.get_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )


class AbstractBaseDocument(AbstractBaseTimeStampModel):
    name = models.CharField(max_length=255, unique=True, null=False)
    max_file_size_mb = models.IntegerField(default=10)
    allowed_file_types = models.CharField(
        max_length=255,
        default='pdf,jpg,jpeg,png,doc,docx',
        help_text='Comma-separated list of allowed file types (e.g., pdf,jpg,jpeg,png,doc,docx)'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class AbstractSocialMedia(AbstractBaseTimeStampModel):
    class Platform(models.TextChoices):
        FACEBOOK = "facebook", "Facebook"
        INSTAGRAM = "instagram", "Instagram"
        TWITTER = "twitter", "Twitter"
        LINKEDIN = "linkedin", "LinkedIn"
        TIKTOK = "tiktok", "TikTok"
        YOUTUBE = "youtube", "YouTube"
        WEBSITE = "website", "Website"
        TELEGRAM = "telegram", "Telegram"
        WHATSAPP = "whatsapp", "Whatsapp"

    platform = models.CharField(
        max_length=250,
        choices=Platform.choices
    )
    username = models.CharField(max_length=255, blank=True, null=True)
    profile_url = models.URLField(max_length=800)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.get_platform_display()} - {self.profile_url}"


class AbstractWorkingHour(AbstractBaseTimeStampModel):
    DAY_CHOICES = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    ]

    day_of_week = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        abstract = True
        ordering = ["day_of_week", "start_time"]

    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.start_time} - {self.end_time}"


class User(AbstractUser, AbstractBaseTimeStampModel):
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
        PATIENT = "PATIENT", "Patient"
        CLINIC = "CLINIC", "Clinic"

    base_role = Role.SUPERADMIN
    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        db_index=True,
        null=True,
        blank=True,
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
            else:
                self.phone_number = self.username
        super().save(*args, **kwargs)


    def get_full_name(self):
        return super().get_full_name()

    @staticmethod
    def generate_verification_code(length=4) -> str:
        return "".join(random.choices(string.digits, k=length))  # noqa: S311

    def send_verification_email(self):
        code = self.generate_verification_code()
        self.email_code = code
        self.save(update_fields=["email_code"])

        send_mail(
            "Your Medbook Verification Code",
            f"Your email verification code is: {code}",
            os.getenv("EMAIL_HOST_USER"),
            [self.email],
            fail_silently=False,
        )

    def send_verification_sms(self):
        code = self.generate_verification_code()
        self.email_code = code
        self.save(update_fields=["email_code"])

        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=f"Your verification code is: {code}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=self.phone_number,
            )
        except Exception:
            raise Exception("Twilio not activated. Use email instead.")  # noqa: B904

    def __str__(self):
        return f"{self.id} - {self.username}"


class Specialty(AbstractBaseTimeStampModel):
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

    class Meta:
        verbose_name = "Specialty"
        verbose_name_plural = "Specialties"


class Clinic(AbstractBaseTimeStampModel):
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


class Doctor(AbstractBaseTimeStampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
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
    bio = models.TextField(blank=True, null=True)
    profile_image_url = models.TextField(blank=True, null=True)
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
        return f"{self.id} - {self.user.first_name} - {self.user.last_name}"


class DoctorCertificate(AbstractBaseTimeStampModel):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="certificates"
    )
    certificate_type = models.CharField(max_length=255, null=False)
    title = models.CharField(max_length=255, null=False)
    issuing_organization = models.CharField(max_length=255, null=False)
    issue_date = models.DateField(null=False)
    expiry_date = models.DateField(null=True, blank=True)
    certificate_number = models.CharField(max_length=255, null=True, blank=True)
    file_url = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_certificates",
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.title} - {self.doctor}"

    class Meta:
        verbose_name = "Doctor Certificate"
        verbose_name_plural = "Doctor Certificates"


class DoctorLanguage(AbstractBaseTimeStampModel):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="languages"
    )
    language_code = models.CharField(max_length=5, null=False)
    language_name = models.CharField(max_length=255, null=False)
    proficiency_level = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.language_name} - {self.doctor}"

    class Meta:
        verbose_name = "Doctor Language"
        verbose_name_plural = "Doctor Languages"


class DoctorService(AbstractBaseTimeStampModel):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="services"
    )
    service_name = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.service_name} - {self.doctor}"

    class Meta:
        verbose_name = "Doctor Service"
        verbose_name_plural = "Doctor Services"


class DoctorEducation(AbstractBaseTimeStampModel):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="education"
    )
    degree = models.CharField(max_length=255, null=False)
    position = models.CharField(max_length=255, blank=True, null=True)
    field_of_study = models.CharField(max_length=255, null=False)
    institution_name = models.CharField(max_length=255, null=False)
    institution_location = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    honors_awards = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.degree} - {self.doctor}"
    
    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be earlier than start date.")

    class Meta:
        verbose_name = "Doctor Education"
        verbose_name_plural = "Doctor Educations"


class DoctorExperience(AbstractBaseTimeStampModel):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="experience"
    )
    position = models.CharField(max_length=255, null=False)
    organization_name = models.CharField(max_length=255, null=False)
    organization_type = models.CharField(max_length=255, null=True, blank=True)
    organization_location = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    total_years = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )

    def __str__(self):
        return f"{self.id} at {self.position} - {self.doctor}"

    class Meta:
        verbose_name = "Doctor Experience"
        verbose_name_plural = "Doctor Experience"


class Address(AbstractBaseAddress):
    clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, related_name="addresses"
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="addresses"
    )

    def __str__(self):
        return f"{self.id} - {self.address_line_1}, {self.state} - {self.clinic}"

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class Patient(AbstractBaseTimeStampModel):
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

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"


class PatientAddress(AbstractBaseAddress):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="addresses"
    )

    def __str__(self):
        return f"{self.id}, {self.address_line_1}, {self.state} - {self.patient}"

    class Meta:
        verbose_name = "Patient Address"
        verbose_name_plural = "Patient Addresses"


class Appointment(AbstractBaseTimeStampModel):
    class AppointmentType(models.TextChoices):
        IN_PERSON = "in_person", "In Person"
        ONLINE_VIDEO = "online_video", "Online Video"
        ONLINE_CHAT = "online_chat", "Online Chat"
        PHONE = "phone", "Phone"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"
        NO_SHOW = "no_show", "No Show"

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="appointments"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments"
    )
    clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, related_name="appointments"
    )
    services = models.ManyToManyField(DoctorService)
    appointment_type = models.CharField(
        max_length=20, choices=AppointmentType.choices, null=True, blank=True
    )
    appointment_date = models.DateField(null=False)
    appointment_time = models.TimeField(null=False)
    duration_minutes = models.IntegerField(default=30)
    status = models.CharField(
        max_length=20, choices=Status.choices, null=True, blank=True
    )
    cancellation_reason = models.TextField(null=True, blank=True)
    patient_notes = models.TextField(null=True, blank=True)
    doctor_notes = models.TextField(null=True, blank=True)
    is_reminder_sent = models.BooleanField(default=False)
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="only if appointment is online",
    )

    def __str__(self):
        return f"{self.id} - {self.patient} appointed on {self.doctor}"

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"


class Review(AbstractBaseTimeStampModel):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="reviews"
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reviews")
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="reviews")
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    rating = models.FloatField(null=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    would_recommend = models.BooleanField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Review {self.rating} stars by {self.patient} for {self.doctor}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class ClinicImage(AbstractBaseImage):
    instance = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, related_name="clinic_images"
    )

    def __str__(self):
        return f"Clinic: {self.instance.id} | {self.image}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.instance, 'profile_image_url'):
            self.instance.profile_image_url = self.image.url
            self.instance.save()

    class Meta:
        verbose_name = "Clinic Image"
        verbose_name_plural = "Clinic Images"


class DoctorImage(AbstractBaseImage):
    instance = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="doctor_images"
    )

    def __str__(self):
        return f"Doctor: {self.instance.id} | {self.image}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.instance, 'profile_image_url'):
            self.instance.profile_image_url = self.image.url
            self.instance.save()

    class Meta:
        verbose_name = "Doctor Image"
        verbose_name_plural = "Doctor Images"


class PatientImage(AbstractBaseImage):
    instance = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="patient_images"
    )

    def __str__(self):
        return f"Patient: {self.instance.id} | {self.image}"

    class Meta:
        verbose_name = "Patient Image"
        verbose_name_plural = "Patient Images"


class DoctorDocument(AbstractBaseDocument):
    instance = models.ForeignKey(
        'Doctor', on_delete=models.CASCADE, related_name="doctor_documents"
    )
    file = models.FileField(
        upload_to="doctor_documents_/%Y/%m/%d/",
        validators=[FileExtensionValidator(
            allowed_extensions=[
                "jpg", "jpeg", "png", "pdf", "docx", "doc"
            ])],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Doctor: {self.instance.id} | Document: {self.name}"

    class Meta:
        verbose_name = "Doctor Document"
        verbose_name_plural = "Doctor Documents"


class ClinicDocument(AbstractBaseDocument):
    instance = models.ForeignKey(
        'Clinic', on_delete=models.CASCADE, related_name="clinic_documents"
    )
    file = models.FileField(
        upload_to="clinic_documents_/%Y/%m/%d/",
        validators=[FileExtensionValidator(
            allowed_extensions=[
                "jpg", "jpeg", "png", "pdf", "docx", "doc"
            ])],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Clinic: {self.instance.id} | Document: {self.name}"

    class Meta:
        verbose_name = "Clinic Document"
        verbose_name_plural = "Clinic Documents"


class DocumentVerificationHistory(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
        ('incomplete', 'Incomplete'),
        ('resubmitted', 'Resubmitted'),
    ]

    document_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=False,
        limit_choices_to={'model__in': ('doctordocument', 'clinicdocument')}
    )
    verified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name="document_verifications", null=False
    )
    document_id = models.BigIntegerField(null=False)
    content_object = GenericForeignKey('document_type', 'document_id')
    old_status = models.CharField(max_length=255, choices=STATUS_CHOICES, blank=True, null=True)
    new_status = models.CharField(max_length=255, choices=STATUS_CHOICES, null=False)
    verification_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.document_type.name} ID: {self.document_id} | {self.new_status} by {self.verified_by}"

    class Meta:
        verbose_name = "Document Verification History"
        verbose_name_plural = "Document Verification History"


class DoctorSocialMedia(AbstractSocialMedia):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="doctor_social_media"
    )
    class Meta:
        verbose_name = "Doctor Social Media"
        verbose_name_plural = "Doctor Social Media Links"


class ClinicSocialMedia(AbstractSocialMedia):
    clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, related_name="clinic_social_media"
    )
    class Meta:
        verbose_name = "Clinic Social Media"
        verbose_name_plural = "Clinic Social Media Links"


class DoctorWorkingHour(AbstractWorkingHour):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="working_hours"
    )

    class Meta:
        verbose_name = "Doctor Working Hour"
        verbose_name_plural = "Doctor Working Hours"


class ClinicWorkingHour(AbstractWorkingHour):
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        related_name="working_hours"
    )

    class Meta:
        verbose_name = "Clinic Working Hour"
        verbose_name_plural = "Clinic Working Hours"


class MedicalTest(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    TYPE_CHOICES = (
        ("Online", "Online"),
        ("Offline", "Offline"),
    )

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Paid Now", "Paid Now"),
        ("Success", "Success"),
        ("Cancelled", "Cancelled"),
    )

    id = models.BigAutoField(primary_key=True)

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medbook_bookings"
    )
    doctor = models.ForeignKey(
        "medbook.Doctor",
        on_delete=models.SET_NULL,
        null=True,
        related_name="medbook_bookings"
    )

    appointment_number = models.CharField(max_length=50, unique=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(null=True, blank=True)
    cancellation_reason = models.TextField(null=True, blank=True)

    can_cancel = models.BooleanField(default=True)
    can_reschedule = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "medbook_bookings"
        ordering = ["-appointment_date", "-appointment_time"]

    def __str__(self):
        return f"{self.appointment_number} ({self.status})"



class Chat(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_chats"
    )
    doctor = models.ForeignKey(
        "medbook.Doctor",
        on_delete=models.CASCADE,
        related_name="doctor_chats"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('patient', 'doctor')
        db_table = "medbook_chats"
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['patient', '-updated_at']),
            models.Index(fields=['doctor', '-updated_at']),
        ]

    def __str__(self):
        return f"Chat {self.patient.get_full_name()} - Dr.{self.doctor.user.get_full_name()}"


class Message(models.Model):
    class SenderType(models.TextChoices):
        PATIENT = "patient", "Patient"
        DOCTOR = "doctor", "Doctor"

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_chat_messages"
    )
    sender_type = models.CharField(max_length=10, choices=SenderType.choices)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "medbook_messages"
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['chat', '-created_at']),
            models.Index(fields=['is_read', 'sender_type']),
        ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.chat.updated_at = self.created_at
            self.chat.save(update_fields=['updated_at'])

    def __str__(self):
        return f"{self.get_sender_type_display()}: {self.content[:30]}"