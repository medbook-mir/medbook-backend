from django.contrib.auth import get_user_model
from django.http import JsonResponse
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import MedicalTest
from .serializers import (
    DoctorOrClinicSignupSerializer,
    SendOTPSerializer,
    TestSerializer,
    VerifyOTPSerializer,
)

User = get_user_model()


def health_check(request):
    return JsonResponse({"status": "ok"})


class TestListView(generics.ListAPIView):
    queryset = MedicalTest.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Test API",
        description="Это защищенный эндпоинт для получения списка медицинских тестов. Требуется аутентификация.",
        responses={200: TestSerializer(many=True)},
        tags=["API Test"],
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"message": "Это защищенный эндпоинт", "data": serializer.data})


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        operation_id="token_obtain_pair",
        summary="Token obtain API",
        description="Получение JWT токена по username и password",
        request=TokenObtainPairSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "refresh": {"type": "string"},
                        "access": {"type": "string"},
                    },
                },
                description="Токены получены",
            ),
            400: OpenApiResponse(description="Неверные учетные данные"),
        },
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @extend_schema(
        operation_id="token_refresh",
        summary="Token refresh API",
        description="Refresh JWT access token using a valid refresh token",
        request=TokenRefreshSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "access": {
                            "type": "string",
                            "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM4MzYwNjAwLCJpYXQiOjE2MzgzNTcwMDAsImp0aSI6ImFiY2RlZmdoaWprbG1ub3AiLCJ1c2VyX2lkIjoxfQ.xyz123",
                            "description": "New access token",
                        },
                        "refresh": {
                            "type": "string",
                            "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzODQ0MzQwMCwiaWF0IjoxNjM4MzU3MDAwLCJqdGkiOiJhYmNkZWZnaGlqa2xtbm9wIiwidXNlcl9pZCI6MX0.abc456",
                            "description": "New refresh token (only if ROTATE_REFRESH_TOKENS is True)",
                        },
                    },
                    "required": ["access"],
                },
                description="Token refreshed successfully",
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "refresh": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["This field is required."],
                        },
                        "detail": {
                            "type": "string",
                            "example": "Token is invalid or expired",
                        },
                        "code": {"type": "string", "example": "token_not_valid"},
                    },
                },
                description="Invalid or expired refresh token",
            ),
        },
        examples=[
            OpenApiExample(
                name="Token Refresh Request",
                value={
                    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzODQ0MzQwMCwiaWF0IjoxNjM4MzU3MDAwLCJqdGkiOiJhYmNkZWZnaGlqa2xtbm9wIiwidXNlcl9pZCI6MX0.abc456"
                },
                request_only=True,
            )
        ],
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SendOTPView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="send_otp",
        summary="Patient Signup API",
        request=SendOTPSerializer,
        responses={
            201: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "example": "Verification code sent to email. Check your email for the code.",
                        },
                        "user_id": {
                            "type": "integer",
                            "example": 123,
                            "description": "ID of the created user",
                        },
                        "email": {
                            "type": "string",
                            "example": "test@gmail.com",
                            "description": "Email where verification code was sent",
                        },
                        "expires_at": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2025-07-10T15:30:00Z",
                            "description": "When the verification code expires",
                        },
                    },
                    "required": ["message"],
                },
                description="Verification code sent successfully",
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "field_name": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["This field is required."],
                        },
                        "non_field_errors": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["Passwords do not match."],
                        },
                    },
                    "additionalProperties": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                description="Validation errors",
            ),
        },
        description=(
            "Register a new user with required fields. "
            "A verification code will be sent to the email or phone number for account activation."
        ),
        examples=[
            OpenApiExample(
                name="Email Registration",
                value={
                    "username": "test@gmail.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "birthday": "26-02-1990",
                    "password": "strong_password123",
                    "repeat_password": "strong_password123",
                },
                request_only=True,
            ),
            OpenApiExample(
                name="Phone Registration",
                value={
                    "username": "+998901234567",
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "birthday": "15-05-1995",
                    "password": "secure_pass456",
                    "repeat_password": "secure_pass456",
                },
                request_only=True,
            ),
        ],
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Verification code sent to email. Check your email for the code."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="verify_otp",
        summary="Verifcation code API",
        request=VerifyOTPSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "example": "Verification successful.",
                        }
                    },
                    "required": ["message"],
                },
                description="Verification successful, account activated",
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "email_code": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["This field is required."],
                        },
                        "error": {
                            "type": "string",
                            "example": "Invalid or expired verification code",
                        },
                    },
                },
                description="Invalid verification code, expired code, or validation errors",
            ),
        },
        description="Verify user account by submitting the email verification code received during registration.",
        examples=[
            OpenApiExample(
                name="Valid Verification Code",
                value={"email_code": "1234"},
                request_only=True,
            ),
            OpenApiExample(
                name="With Email (if required)",
                value={"email": "test@gmail.com", "email_code": "1234"},
                request_only=True,
            ),
        ],
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email_code = serializer.validated_data["email_code"]
            try:
                user = User.objects.get(email_code=email_code)
                if not user.is_active:
                    user.is_active = True
                    user.email_code = None
                    user.save()
                    return Response(
                        {"message": "Verification successful. You can now log in."},
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    {"message": "Account already verified."},
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid verification code."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorOrClinicSignupView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="doctor_clinic_signup",
        summary="Doctor and Clinic Signup API",
        request=DoctorOrClinicSignupSerializer,
        responses={
            201: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "example": "Verification code sent to email. Check your email for the code.",
                        }
                    },
                    "required": ["message"],
                },
                description="Registration successful, verification code sent",
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "role": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["This field is required."],
                        },
                        "email": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["Enter a valid email address."],
                        },
                        "first_name": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["This field is required."],
                        },
                        "clinic_name": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["This field is required."],
                        },
                        "password": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": [
                                "This password is too short. It must contain at least 8 characters."
                            ],
                        },
                        "non_field_errors": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["User with this email already exists."],
                        },
                    },
                },
                description="Validation errors or user already exists",
            ),
        },
        description=(
            "Register a new doctor or clinic with required fields. "
            "A verification code will be sent to the email address for account activation. "
            "The role field determines whether to create a doctor or clinic profile."
        ),
        examples=[
            OpenApiExample(
                name="Doctor Signup",
                value={
                    "role": "doctor",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john@example.com",
                    "password": "strong_password123",
                },
                request_only=True,
            ),
            OpenApiExample(
                name="Clinic Signup",
                value={
                    "role": "clinic",
                    "clinic_name": "Health Plus Medical Center",
                    "email": "clinic@healthplus.com",
                    "password": "secure_clinic_pass123",
                },
                request_only=True,
            ),
        ],
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = DoctorOrClinicSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Verification code sent to email. Check your email for the code."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
