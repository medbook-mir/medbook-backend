import random
import re
import string
from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers
from twilio.rest import Client

from .models import MedicalTest

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
            "birthday",
            "date_joined",
            "password",
            "repeat_password",
        ]
        extra_kwargs = {
            "username": {"required": True},
            "password": {"write_only": True},
            "repeat_password": {"write_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "birthday": {"required": True},
            "date_joined": {"read_only": True},
        }

    def create(self, validated_data):
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        validated_data.pop("repeat_password")

        user = User(username=username, **validated_data)
        user.set_password(password)
        user.is_active = False
        verification_code = "".join(random.choices(string.digits, k=4))
        user.verification_code = verification_code

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(email_pattern, username):
            user.email = username
        else:
            user.phone_number = username

        user.save()

        if user.email:
            send_mail(
                "Your Medbook Verification Code",
                f"Your email verification code is: {verification_code}",
                "contact@medvisit.uz",
                [user.email],
                fail_silently=False,
            )
        elif user.phone_number:
            self.send_verification_sms(user.phone_number, verification_code)
        return user

    def send_verification_sms(self, phone_number, code):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your verification code is: {code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number,
        )
        return message.sid


class VerifyOTPSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=4)


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalTest
        fields = ["id", "name", "age", "created_at"]
