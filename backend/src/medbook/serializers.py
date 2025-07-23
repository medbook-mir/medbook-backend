import re
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers

from .models import Clinic, Doctor, MedicalTest, Patient

User = get_user_model()


class SendOTPSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    repeat_password = serializers.CharField(write_only=True, required=True)
    birthday = serializers.DateField(required=True, input_formats=["%d-%m-%Y"])

    def validate_username(self, value):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        phone_pattern = r"^\+?[\d\s-]{9,15}$"

        if not (re.match(email_pattern, value) or re.match(phone_pattern, value)):
            raise serializers.ValidationError(
                "Please enter a valid email or phone number."
            )

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This contact is already registered.")
        return value

    def validate_password(self, value):
        repeat_password = self.initial_data.get("repeat_password")
        if value != repeat_password:
            raise serializers.ValidationError("Passwords do not match.")
        return value

    def validate_birthday(self, value):
        today = date.today()

        if value > today:
            raise serializers.ValidationError("Birthday cannot be in the future.")
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
            raise serializers.ValidationError("A user with this email already exists.")
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


class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    specialty = serializers.SerializerMethodField()
    clinic = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            "id",
            "user",
            "clinic",
            "license_number",
            "consultation_fee",
            "online_consultation_fee",
            "average_consultation_time",
            "is_online_consultation_available",
            "rating",
            "total_reviews",
            "total_patients",
            "bio",
            "years_of_experience",
            "specialty",
            "is_primary",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def get_user(self, obj):
        if obj.user:
            return {
                "id": obj.user.id,
                "first_name": obj.user.first_name,
                "last_name": obj.user.last_name,
                "email": obj.user.email,
                "phone_number": obj.user.phone_number,
                "gender": obj.user.gender,
                "profile_image_url": obj.user.profile_image_url,
                "is_verified": obj.user.is_verified,
            }
        return None

    def get_specialty(self, obj):
        if obj.specialty:
            return {
                "id": obj.specialty.id,
                "name": obj.specialty.name,
                "description": obj.specialty.description,
                "category": obj.specialty.category,
            }
        return None

    def get_clinic(self, obj):
        if obj.clinic:
            return {
                "id": obj.clinic.id,
                "name": obj.clinic.name,
                "website_url": obj.clinic.website_url,
                "profile_image_url": obj.clinic.profile_image_url,
                "description": obj.clinic.description,
                "established_year": obj.clinic.established_year,
                "total_staff": obj.clinic.total_staff,
            }
        return None


class DoctorDetailSerializer(DoctorSerializer):
    """Extended serializer for detailed doctor information"""
    
    class Meta(DoctorSerializer.Meta):
        fields = DoctorSerializer.Meta.fields + [
            "verified_by",
        ]

    def get_verified_by(self, obj):
        if obj.verified_by:
            return {
                "id": obj.verified_by.id,
                "first_name": obj.verified_by.first_name,
                "last_name": obj.verified_by.last_name,
            }
        return None
