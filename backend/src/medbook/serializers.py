import re
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema_field, OpenApiTypes

from .models import (
    Clinic, 
    ClinicDocument, 
    ClinicImage, 
    ClinicSocialMedia, 
    ClinicWorkingHour, 
    Doctor, 
    DoctorCertificate, 
    DoctorDocument, 
    DoctorEducation, 
    DoctorExperience, 
    DoctorImage, 
    DoctorLanguage, 
    DoctorService, 
    DoctorSocialMedia, 
    DoctorWorkingHour, 
    MedicalTest, 
    Patient, 
    PatientImage, 
    Review,
    Address,
    Specialty
)

User = get_user_model()


class StandardResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField(required=False)


class ListResponseSerializer(StandardResponseSerializer):
    data = serializers.ListField(child=serializers.DictField())
    count = serializers.IntegerField()


class DetailResponseSerializer(StandardResponseSerializer):
    data = serializers.DictField()


class ErrorResponseSerializer(StandardResponseSerializer):
    errors = serializers.DictField()


class SendOTPSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    repeat_password = serializers.CharField(write_only=True, required=True)
    birthday = serializers.DateField(required=True, input_formats=["%d-%m-%Y"])

    def validate_username(self, value):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        phone_pattern = r"^\+?[\d\s-]{9,15}$"

        if not (
            re.match(email_pattern, value) or re.match(phone_pattern, value)
        ):
            raise serializers.ValidationError(
                "Please enter a valid email or phone number."
            )

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "This contact is already registered."
            )
        return value

    def validate_password(self, value):
        repeat_password = self.initial_data.get("repeat_password")
        if value != repeat_password:
            raise serializers.ValidationError("Passwords do not match.")
        return value

    def validate_birthday(self, value):
        today = date.today()

        if value > today:
            raise serializers.ValidationError(
                "Birthday cannot be in the future."
            )
        return value

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "birthday",
            "password",
            "repeat_password",
        ]
        extra_kwargs = {
            "username": {"required": True},
            "password": {"write_only": True},
            "repeat_password": {"write_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": False},
            "birthday": {"required": False},
            "phone_number": {"required": False},
            "date_joined": {"read_only": True},
        }

    def create(self, validated_data):
        with transaction.atomic():
            username = validated_data.pop("username")
            password = validated_data.pop("password")
            validated_data.pop("repeat_password")
            birthday = validated_data.pop("birthday", None)

            user = User(username=username, **validated_data)
            user.set_password(password)
            user.is_active = False

            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if re.match(email_pattern, username):
                user.email = username
            else:
                user.phone_number = username

            user.save()

            Patient.objects.create(user=user, birthday=birthday)

            if user.email:
                user.send_verification_email()
            elif user.phone_number:
                user.send_verification_sms()

            return user


class VerifyOTPSerializer(serializers.Serializer):
    email_code = serializers.CharField(max_length=4)


class DoctorOrClinicSignupSerializer(serializers.ModelSerializer):
    clinic_name = serializers.CharField(required=False)
    role = serializers.CharField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def validate(self, data):
        role = data.get("role")

        if role == "doctor":
            if not data.get("first_name") or not data.get("last_name"):
                raise serializers.ValidationError(
                    "Doctor must have first name and last name."
                )
        elif role == "clinic":
            if not data.get("clinic_name"):
                raise serializers.ValidationError(
                    "Clinic must have a clinic_name field."
                )
        else:
            raise serializers.ValidationError("Invalid or missing role.")

        return data

    class Meta:
        model = User
        fields = [
            "role",
            "first_name",
            "last_name",
            "clinic_name",
            "email",
            "password",
            "created_at",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "created_at": {"read_only": True},
        }

    def create(self, validated_data):
        role = validated_data.pop("role")

        with transaction.atomic():
            if role == "doctor":
                user = User.objects.create(
                    first_name=validated_data["first_name"],
                    last_name=validated_data["last_name"],
                    username=validated_data["email"],
                    email=validated_data["email"],
                    password=make_password(validated_data["password"]),
                )
                user.is_active = False
                user.save()

                Doctor.objects.create(user=user)

                if user.email:
                    user.send_verification_email()

                return user

            elif role == "clinic":
                clinic_name = validated_data.pop("clinic_name")
                user = User.objects.create(
                    first_name="",
                    last_name="",
                    username=validated_data["email"],
                    email=validated_data["email"],
                    password=make_password(validated_data["password"]),
                )
                user.is_active = False
                user.save()

                Clinic.objects.create(user=user, name=clinic_name)

                if user.email:
                    user.send_verification_email()

                return user


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalTest
        fields = ["id", "name", "age", "created_at"]


class UserInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField(required=False)
    profile_image = serializers.URLField(required=False)
    is_verified = serializers.BooleanField()


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ["id", "name", "category", "description", "is_active"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['updated_at']
        read_only_fields = ('id', 'created_at')

    def validate(self, data):
        doctor = data.get('doctor')
        clinic = data.get('clinic')
        
        if not doctor and not clinic:
            raise serializers.ValidationError("Either doctor or clinic must be specified")
        
        if doctor and clinic:
            raise serializers.ValidationError("Cannot specify both doctor and clinic")
            
        return data


class VerifiedBySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class DoctorShortSerializer(serializers.ModelSerializer):
    doctor_id = serializers.IntegerField(source="id")
    user = UserInfoSerializer(read_only=True)
    specialty = SpecialtySerializer(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ["doctor_id", "user", "specialty", "address"]


class BaseImageSerializer(serializers.ModelSerializer):
    instance_model = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not self.instance_model:
            raise ValueError(f"{self.__class__.__name__} must define 'instance_model'")

    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise ValidationError("User must be authenticated")

        try:
            instance = self.instance_model.objects.get(user=request.user)
            attrs['instance'] = instance
        except self.instance_model.DoesNotExist:
            raise ValidationError(f"No {self.instance_model.__name__} profile found for this user")
        return attrs


class ClinicImageSerializer(BaseImageSerializer):
    instance_model = Clinic
    clinic_id = serializers.IntegerField(source='instance.id', read_only=True)

    class Meta:
        model = ClinicImage
        fields = ['id',  'clinic_id', 'image', 'status']
        read_only_fields = ['id', 'instance']


class DoctorImageSerializer(BaseImageSerializer):
    instance_model = Doctor
    doctor_id = serializers.IntegerField(source='instance.id', read_only=True)

    class Meta:
        model = DoctorImage
        fields = ['id', 'doctor_id', 'image', 'status']
        read_only_fields = ['id', 'instance']


class PatientImageSerializer(BaseImageSerializer):
    instance_model = Patient
    patient_id = serializers.IntegerField(source='instance.id', read_only=True)

    class Meta:
        model = PatientImage
        fields = ['id', 'patient_id', 'image', 'status']
        read_only_fields = ['id', 'instance']


class BaseDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id', 
            'instance',
            'file',
            'name', 
            'is_active', 
            'created_at', 
        ]
        read_only_fields = ['id', 'instance', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        if hasattr(instance, 'instance') and instance.instance:
            model_name = instance.instance.__class__.__name__.lower()
            field_name = f"{model_name}_id"
            data[field_name] = data.pop('instance')
        
        return data


class DoctorDocumentSerializer(BaseDocumentSerializer):
    class Meta(BaseDocumentSerializer.Meta):
        model = DoctorDocument
        fields = BaseDocumentSerializer.Meta.fields

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            doctor = Doctor.objects.get(user=user)
            validated_data['instance'] = doctor
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("No doctor profile found for this user")
        
        return super().create(validated_data)


class ClinicDocumentSerializer(BaseDocumentSerializer):
    class Meta(BaseDocumentSerializer.Meta):
        model = ClinicDocument
        fields = BaseDocumentSerializer.Meta.fields

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            clinic = Clinic.objects.get(user=user)  
            validated_data['instance'] = clinic
        except Clinic.DoesNotExist:
            raise serializers.ValidationError("No clinic profile found for this user") 
        
        return super().create(validated_data)
    

class DoctorCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorCertificate
        exclude = ['updated_at']
        read_only_fields = ['id', 'doctor', 'created_at']

    def validate(self, data):
        if data.get('expiry_date') and data.get('issue_date'):
            if data['expiry_date'] <= data['issue_date']:
                raise serializers.ValidationError("Expiry date must be after issue date.")
        return data


class DoctorLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorLanguage
        fields = [
            'id', 
            'doctor', 
            'language_code', 
            'language_name', 
            'proficiency_level', 
            'created_at'
        ]
        read_only_fields = ['id', 'doctor', 'created_at']

    def validate_language_code(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("Language code cannot exceed 5 characters.")
        return value.lower()
    

class DoctorEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorEducation
        exclude = ['updated_at']
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        doctor = attrs.get("doctor") or getattr(self.instance, "doctor", None)
        if doctor:
            get_object_or_404(Doctor, id=doctor.id, is_active=True)
        return attrs
    

class DoctorServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorService
        exclude = ['updated_at']
        read_only_fields = ('id', 'created_at',)


class DoctorExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorExperience
        exclude = ['updated_at', 'doctor']
        read_only_fields = ('id', 'created_at')


class DoctorSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSocialMedia
        exclude = ("updated_at", 'doctor')


class ClinicSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicSocialMedia
        exclude = ("updated_at", 'clinic')


class DoctorWorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorWorkingHour
        exclude = ("updated_at", 'doctor')


class ClinicWorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicWorkingHour
        exclude = ("updated_at", 'clinic')


class ReviewSerializer(serializers.ModelSerializer):
    clinic_name = serializers.CharField(source="clinic.name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.full_name", read_only=True)
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "patient",
            "patient_name",
            "doctor",
            "doctor_name",
            "clinic",
            "clinic_name",
            "appointment",
            "rating",
            "title",
            "comment",
            "would_recommend",
            "is_verified",
            "is_anonymous",
            "helpful_count",
            "is_active",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "is_verified",
            "helpful_count",
            "created_at",
        ]


class ReviewShortSerializer(serializers.ModelSerializer):
    patient_full_name = serializers.SerializerMethodField()
    patient_image = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "patient",
            "patient_full_name",
            'patient_image',
            "rating",
            "comment",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_patient_full_name(self, obj):
        return obj.patient.user.get_full_name() if obj.patient else None

    @extend_schema_field(OpenApiTypes.STR)
    def get_patient_image(self, obj):
        if obj.patient:
            image = obj.patient.patient_images.first()
            if image and hasattr(image, "image"):
                return image.image.url
        return None
    

class DayScheduleSerializer(serializers.Serializer):
    start_time = serializers.TimeField(required=False, allow_null=True)
    end_time = serializers.TimeField(required=False, allow_null=True)


class WorkingHoursSerializer(serializers.Serializer):
    monday = DayScheduleSerializer(read_only=True)
    tuesday = DayScheduleSerializer(read_only=True)
    wednesday = DayScheduleSerializer(read_only=True)
    thursday = DayScheduleSerializer(read_only=True)
    friday = DayScheduleSerializer(read_only=True)
    saturday = DayScheduleSerializer(read_only=True)
    sunday = DayScheduleSerializer(read_only=True)


class DoctorDetailSerializer(DoctorShortSerializer):
    verified_by = VerifiedBySerializer(read_only=True)
    experience = DoctorExperienceSerializer(many=True, read_only=True)
    certificates = DoctorCertificateSerializer(many=True, read_only=True)
    services = DoctorServiceSerializer(many=True, read_only=True)
    languages = DoctorLanguageSerializer(many=True, read_only=True)
    working_hours = WorkingHoursSerializer(read_only=True)
    education = DoctorEducationSerializer(many=True, read_only=True)
    social_media = DoctorSocialMediaSerializer(read_only=True)
    reviews = ReviewShortSerializer(many=True, read_only=True)
    online_consultation_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    consultation_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    average_consultation_time = serializers.IntegerField(read_only=True)
    is_online_consultation_available = serializers.BooleanField(read_only=True)
    bio = serializers.CharField(read_only=True)

    class Meta(DoctorShortSerializer.Meta):
        fields = DoctorShortSerializer.Meta.fields + [
            'doctor_id',
            'user', 
            'specialty',
            'address',
            'verified_by', 
            'experience',
            'certificates',
            'services',
            'languages',
            'working_hours',
            'education',
            'social_media',
            'reviews',
            'online_consultation_fee',
            'consultation_fee',
            'average_consultation_time',
            'is_online_consultation_available',
            'bio',
        ]
    
class UpdatePatientProfileSerializer(serializers.Serializer):
    fullName = serializers.CharField(max_length=255)
    dateOfBirth = serializers.DateField()
    phoneNumber = serializers.CharField(max_length=20)
    gender = serializers.ChoiceField(choices=["Male", "Female", "Other"])
    email = serializers.EmailField()

from rest_framework import serializers
from .models import Doctor
from django.conf import settings

class DoctorSerializer(serializers.ModelSerializer):
    fullName = serializers.SerializerMethodField()
    specialty = serializers.CharField(source="specialty.name", default=None)
    clinic = serializers.CharField(source="clinic.name", default=None)
    profileImageUrl = serializers.CharField(source="profile_image_url", default=None)

    class Meta:
        model = Doctor
        fields = ["id", "fullName", "specialty", "clinic", "profileImageUrl"]

    def get_fullName(self, obj):
        return obj.user.get_full_name() if obj.user else None


from django.contrib.auth import get_user_model
User = get_user_model()

class PatientSerializer(serializers.ModelSerializer):
    fullName = serializers.SerializerMethodField()
    phoneNumber = serializers.CharField(source="phone_number", default=None)
    email = serializers.EmailField(default=None)

    class Meta:
        model = User
        fields = ["id", "fullName", "phoneNumber", "email"]

    def get_fullName(self, obj):
        return obj.get_full_name() if obj else None

from .models import Booking, Doctor

class BookingSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    patient = PatientSerializer()
    appointmentNumber = serializers.CharField(source="appointment_number")
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    canCancel = serializers.BooleanField(source="can_cancel")
    canReschedule = serializers.BooleanField(source="can_reschedule")
    createdAt = serializers.DateTimeField(source="created_at", format="%d.%m.%Y %H:%M")
    updatedAt = serializers.DateTimeField(source="updated_at", format="%d.%m.%Y %H:%M")
    cancelledAt = serializers.DateTimeField(source="cancelled_at", format="%d.%m.%Y %H:%M", default=None)

    class Meta:
        model = Booking
        fields = [
            "id",
            "appointmentNumber",
            "date",
            "time",
            "type",
            "status",
            "notes",
            "canCancel",
            "canReschedule",
            "doctor",
            "patient",
            "createdAt",
            "updatedAt",
            "cancelledAt",
        ]

    def get_date(self, obj):
        return obj.appointment_date.strftime("%Y-%m-%d")

    def get_time(self, obj):
        return obj.appointment_time.strftime("%H:%M")

class BookingCreateSerializer(serializers.Serializer):
    doctorId = serializers.IntegerField()
    appointmentDate = serializers.DateField()
    appointmentTime = serializers.TimeField(
        input_formats=["%H:%M", "%H:%M:%S"]
    )
    type = serializers.ChoiceField(choices=["online", "offline"])
    notes = serializers.CharField(required=False, allow_blank=True)


class BookingCancelSerializer(serializers.Serializer):
    cancellationReason = serializers.CharField(
        max_length=500,
        required=True,
        allow_blank=False,
        help_text="Reason why the booking is being cancelled"
    )

class BookingRescheduleSerializer(serializers.Serializer):
    newDate = serializers.DateField(format="%Y-%m-%d")
    newTime = serializers.TimeField(
        input_formats=['%H:%M', '%H:%M:%S', '%H:%M:%S.%f']
    )