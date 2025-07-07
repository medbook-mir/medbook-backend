import random
import re
import string
from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import transaction
from rest_framework import serializers
from twilio.rest import Client

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
            email_code = "".join(random.choices(string.digits, k=4))
            user.email_code = email_code

            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if re.match(email_pattern, username):
                user.email = username
            else:
                user.phone_number = username

            user.save()

            Patient.objects.create(user=user, birthday=birthday)

            if user.email:
                send_mail(
                    "Your Medbook Verification Code",
                    f"Your email verification code is: {email_code}",
                    "example@gmail.com",
                    [user.email],
                    fail_silently=False,
                )
            elif user.phone_number:
                self.send_verification_sms(user.phone_number, email_code)
            return user

    def send_verification_sms(self, phone_number, code):
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Your verification code is: {code}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number,
            )
            return message.sid
        except Exception:
            raise serializers.ValidationError(
                "Twilio account has not been activated yet. Use email instead."
            )


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
                doctor = Doctor.objects.create(user=user)
                return {
                    "user_id": user.id,
                    "doctor_id": doctor.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": role,
                    "created_at": doctor.created_at,
                }

            elif role == "clinic":
                clinic_name = validated_data.pop("clinic_name")
                user = User.objects.create(
                    first_name="",
                    last_name="",
                    username=validated_data["email"],
                    email=validated_data["email"],
                    password=make_password(validated_data["password"]),
                )
                clinic = Clinic.objects.create(user=user, name=clinic_name)
                return {
                    "clinic_id": clinic.id,
                    "email": user.email,
                    "clinic_name": clinic.name,
                    "role": role,
                    "created_at": clinic.created_at,
                }


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalTest
        fields = ["id", "name", "age", "created_at"]
