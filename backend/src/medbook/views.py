from django.contrib.auth import get_user_model
from django.http import JsonResponse
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        request=TokenObtainPairSerializer,
        responses={
            200: OpenApiResponse(response=dict, description="Токены получены"),
            400: OpenApiResponse(description="Неверные учетные данные"),
        },
        description="Получение JWT токена по username и password",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TestListView(generics.ListAPIView):
    queryset = MedicalTest.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"message": "Это защищенный эндпоинт", "data": serializer.data})


class SendOTPView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=SendOTPSerializer,
        responses={
            201: OpenApiResponse(response=dict, description="Verification code sent"),
            400: OpenApiResponse(description="Invalid input"),
        },
        description=(
            "Register a new user with required fields. "
            "A verification code will be sent to the email or phone number.",
        ),
        examples=[
            OpenApiExample(
                name="Signup Example",
                value={
                    "username": "test@gmail.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "birthday": "26-02-1990",
                    "password": "strong_password123",
                    "repeat_password": "strong_password123",
                },
                request_only=True,
            )
        ],
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
        request=VerifyOTPSerializer,
        responses={
            200: OpenApiResponse(response=dict, description="Verification successful"),
            400: OpenApiResponse(description="Invalid code or input"),
        },
        description="Verify user by submitting the email verification code.",
        examples=[
            OpenApiExample(
                name="Verification Example",
                value={"email_code": "1234"},
                request_only=True,
            )
        ],
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
        request=DoctorOrClinicSignupSerializer,
        responses={
            201: OpenApiResponse(
                response=dict, description="Registration is successful"
            ),
            400: OpenApiResponse(description="Invalid input"),
        },
        description="Register a new doctor or clinic with required fields",
        examples=[
            OpenApiExample(
                name="Doctor Signup Example",
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
                name="Clinic Signup Example",
                value={
                    "role": "clinic",
                    "clinic_name": "Clinic Name",
                    "email": "clinic@gmail.com",
                    "password": "password",
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request):
        serializer = DoctorOrClinicSignupSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(
                {
                    "message": "Verification code sent to email. Check your email for the code."
                },
                status=status.HTTP_201_CREATED,
            )
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
