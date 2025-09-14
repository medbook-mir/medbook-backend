from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .mixins import (
    BaseCreateRetrieveViewSet,
    BaseListViewSet,
    BaseRetrieveViewSet, 
    BaseViewSet
)
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
    Review
)
from . import serializers as ser
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.core.files.base import ContentFile


User = get_user_model()


def health_check(request):
    return JsonResponse({"status": "ok"})

def test_minio(request):
    file_path = default_storage.save("reports/hello.txt", ContentFile(b"MinIO!"))
    return JsonResponse({"status": "ok", "file_path": file_path})

class TestListView(generics.ListAPIView):
    queryset = MedicalTest.objects.all()
    serializer_class = ser.TestSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Test API",
        description="Это защищенный эндпоинт для получения списка медицинских тестов. Требуется аутентификация.",  # noqa: E501
        responses={200: ser.TestSerializer(many=True)},
        tags=["API Test"],
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"message": "Это защищенный эндпоинт", "data": serializer.data}
        )


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
                            "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM4MzYwNjAwLCJpYXQiOjE2MzgzNTcwMDAsImp0aSI6ImFiY2RlZmdoaWprbG1ub3AiLCJ1c2VyX2lkIjoxfQ.xyz123",  # noqa: E501
                            "description": "New access token",
                        },
                        "refresh": {
                            "type": "string",
                            "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzODQ0MzQwMCwiaWF0IjoxNjM4MzU3MDAwLCJqdGkiOiJhYmNkZWZnaGlqa2xtbm9wIiwidXNlcl9pZCI6MX0.abc456",  # noqa: E501
                            "description": "New refresh token (only if ROTATE_REFRESH_TOKENS is True)",  # noqa: E501
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
                        "code": {
                            "type": "string",
                            "example": "token_not_valid",
                        },
                    },
                },
                description="Invalid or expired refresh token",
            ),
        },
        examples=[
            OpenApiExample(
                name="Token Refresh Request",
                value={
                    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzODQ0MzQwMCwiaWF0IjoxNjM4MzU3MDAwLCJqdGkiOiJhYmNkZWZnaGlqa2xtbm9wIiwidXNlcl9pZCI6MX0.abc456"  # noqa: E501
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
        request=ser.SendOTPSerializer,
        responses={
            201: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "example": "Verification code sent to email. Check your email for the code.",  # noqa: E501
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
            "A verification code will be sent to the email or phone number for account activation."  # noqa: E501
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
        serializer = ser.SendOTPSerializer(data=request.data)
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
        request=ser.VerifyOTPSerializer,
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
        serializer = ser.VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email_code = serializer.validated_data["email_code"]
            try:
                user = User.objects.get(email_code=email_code)
                if not user.is_active:
                    user.is_active = True
                    user.email_code = None
                    user.save()
                    return Response(
                        {
                            "message": "Verification successful. You can now log in."  # noqa: E501
                        },
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
        request=ser.DoctorOrClinicSignupSerializer,
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
                            "example": [
                                "User with this email already exists."
                            ],
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
        serializer = ser.DoctorOrClinicSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Verification code sent to email. Check your email for the code."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorsView(BaseListViewSet):
    queryset = Doctor.objects.all()
    serializer_class = ser.DoctorShortSerializer
    permission_classes = [AllowAny]
    swagger_model = Doctor
    swagger_model_name = 'Doctors'

    def get_queryset(self):
        queryset = Doctor.objects.filter(
            is_active=True,
            is_deleted__isnull=True
        )

        params = self.request.query_params
        specialty_id = params.get("specialty")
        clinic_id = params.get("clinic")
        is_online = params.get("is_online")
        is_primary = params.get("is_primary")

        if specialty_id:
            queryset = queryset.filter(specialty_id=specialty_id)

        if clinic_id:
            queryset = queryset.filter(clinic_id=clinic_id)

        if is_online is not None:
            queryset = queryset.filter(
                is_online_consultation_available=is_online.lower() == "true"
            )

        if is_primary is not None:
            queryset = queryset.filter(is_primary=is_primary.lower() == "true")

        queryset = queryset.order_by("user__first_name", "user__last_name")
        return queryset
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class DoctorByIdView(BaseRetrieveViewSet):
    queryset = Doctor.objects.all()
    serializer_class = ser.DoctorDetailSerializer
    permission_classes = [AllowAny]
    swagger_model = Doctor
    swagger_model_name = 'Doctor'

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch(
                'reviews', 
                queryset=Review.objects
                .select_related('patient__user')
                .prefetch_related('patient__patient_images')
            )
        )

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ClinicImageUploadView(BaseCreateRetrieveViewSet):
    queryset = ClinicImage.objects.all()
    serializer_class = ser.ClinicImageSerializer
    permission_classes = [IsAuthenticated]
    swagger_model = ClinicImage
    swagger_model_name = 'Clinic Images'

    def create(self, request, *args, **kwargs):
        clinic = get_object_or_404(Clinic, user=request.user, is_active=True)

        data = request.data.copy()
        data["clinic"] = clinic.id

        serializer = self.serializer_class(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save() 

        return self.success_response(
            data=serializer.data,
            code=status.HTTP_201_CREATED
        )

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class DoctorImageUploadView(BaseCreateRetrieveViewSet):
    queryset = DoctorImage.objects.all()
    serializer_class = ser.DoctorImageSerializer
    permission_classes = [IsAuthenticated]
    swagger_model = DoctorImage
    swagger_model_name = 'Doctor Images'

    def create(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, user=request.user, is_active=True)

        data = request.data.copy()
        data["doctor"] = doctor.id

        serializer = self.serializer_class(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save() 

        return self.success_response(
            data=serializer.data,
            code=status.HTTP_201_CREATED
        )

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class PatientImageUploadView(BaseCreateRetrieveViewSet):
    queryset = PatientImage.objects.all()
    serializer_class = ser.PatientImageSerializer
    permission_classes = [IsAuthenticated]
    swagger_model = PatientImage
    swagger_model_name = 'Patient Images'

    def create(self, request, *args, **kwargs):
        patient = get_object_or_404(Patient, user=request.user)

        data = request.data.copy()
        data["patient"] = patient.id

        serializer = self.serializer_class(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save() 

        return self.success_response(
            data=serializer.data,
            code=status.HTTP_201_CREATED
        )

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ClinicDocumentUploadView(BaseViewSet):
    serializer_class = ser.ClinicDocumentSerializer
    queryset = ClinicDocument.objects.all()
    permission_classes = [IsAuthenticated]
    swagger_model = ClinicDocument
    swagger_model_name = 'Clinic Documents'

    def get_queryset(self):
        params = self.request.query_params
        clinic_id = params.get('clinic_id')

        queryset = ClinicDocument.objects.select_related(
            'instance', 'instance__user'
        )

        if not self.request.user.is_superuser:
            queryset = queryset.filter(instance__user=self.request.user)

        if clinic_id:
            queryset = queryset.filter(instance_id=clinic_id)

        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            clinict_instance = serializer.validated_data.get('instance')
            if clinict_instance:
                get_object_or_404(Clinic, id=clinict_instance.id, is_active=True)

            document_name = serializer.validated_data.get('name')
            if ClinicDocument.objects.filter(
                instance=clinict_instance,
                name=document_name,
                is_active=True
            ).exists():
                return self.error_response(
                    msg="This document already exists for the doctor",
                    errors={"name": ["Document with this name already exists for this doctor"]},
                    code=status.HTTP_409_CONFLICT
                )

            document = serializer.save()
            return self.success_response(
                data=self.get_serializer(document).data,
                code=status.HTTP_201_CREATED
            )

        return self.error_response(
            msg="Validation failed",
            errors=serializer.errors
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            clinict_instance = serializer.validated_data.get('instance')

            if clinict_instance:
                get_object_or_404(Clinic, id=clinict_instance.id, is_active=True)

            document_name = serializer.validated_data.get('name')
            if clinict_instance and document_name:
                if ClinicDocument.objects.filter(
                    instance=clinict_instance,
                    name=document_name,
                    is_active=True
                ).exclude(id=instance.id).exists():
                    return self.error_response(
                        msg="This document already exists for the doctor",
                        errors={"name": ["Document with this name already exists for this doctor"]},
                        code=status.HTTP_409_CONFLICT
                    )

            document = serializer.save()
            return self.success_response(
                data=self.get_serializer(document).data,
            )

        return self.error_response(
            msg="Validation failed",
            errors=serializer.errors
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            clinict_instance = serializer.validated_data.get('instance', instance.instance)

            if 'instance' in serializer.validated_data:
                get_object_or_404(Clinic, id=clinict_instance.id, is_active=True)

            document_name = serializer.validated_data.get('name', instance.name)
            
            if any(field in serializer.validated_data for field in ('instance', 'name')):
                if ClinicDocument.objects.filter(
                    instance=clinict_instance,
                    name=document_name,
                    is_active=True
                ).exclude(id=instance.id).exists():
                    return self.error_response(
                        msg="This document already exists for the doctor",
                        errors={"name": ["Document with this name already exists for this doctor"]},
                        code=status.HTTP_409_CONFLICT
                    )

            document = serializer.save()
            return self.success_response(
                data=self.get_serializer(document).data,
            )

        return self.error_response(
            msg="Validation failed",
            errors=serializer.errors
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.success_response()
    
    
class DoctorDocumentUploadView(BaseViewSet):
    queryset = DoctorDocument.objects.all()
    serializer_class = ser.DoctorDocumentSerializer
    swagger_model = DoctorDocument
    swagger_model_name = "Doctor Documents"

    def get_queryset(self):
        params = self.request.query_params
        doctor_id = params.get('doctor_id')

        queryset = DoctorDocument.objects.select_related(
            'instance', 'instance__user',
        )

        if not self.request.user.is_superuser:
            queryset = queryset.filter(instance__user=self.request.user)

        if doctor_id:
            queryset = queryset.filter(instance_id=doctor_id)

        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            doctor_instance = serializer.validated_data.get('instance')
            if doctor_instance:
                get_object_or_404(Doctor, id=doctor_instance.id, is_active=True)

            document_name = serializer.validated_data.get('name')
            if DoctorDocument.objects.filter(
                instance=doctor_instance,
                name=document_name,
                is_active=True
            ).exists():
                return self.error_response(
                    msg="This document already exists for the doctor",
                    errors={"name": ["Document with this name already exists for this doctor"]},
                    code=status.HTTP_409_CONFLICT
                )

            document = serializer.save()
            return self.success_response(
                data=self.get_serializer(document).data,
                msg="Doctor document added successfully",
                code=status.HTTP_201_CREATED
            )

        return self.error_response(
            msg="Validation failed",
            errors=serializer.errors
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            doctor_instance = serializer.validated_data.get('instance')

            if doctor_instance:
                get_object_or_404(Doctor, id=doctor_instance.id, is_active=True)

            document_name = serializer.validated_data.get('name')
            if doctor_instance and document_name:
                if DoctorDocument.objects.filter(
                    instance=doctor_instance,
                    name=document_name,
                    is_active=True
                ).exclude(id=instance.id).exists():
                    return self.error_response(
                        msg="This document already exists for the doctor",
                        errors={"name": ["Document with this name already exists for this doctor"]},
                        code=status.HTTP_409_CONFLICT
                    )

            document = serializer.save()
            return self.success_response(
                data=self.get_serializer(document).data,
                msg="Doctor document updated successfully"
            )

        return self.error_response(
            msg="Validation failed",
            errors=serializer.errors
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            doctor_instance = serializer.validated_data.get('instance', instance.instance)

            if 'instance' in serializer.validated_data:
                get_object_or_404(Doctor, id=doctor_instance.id, is_active=True)

            document_name = serializer.validated_data.get('name', instance.name)
            
            if any(field in serializer.validated_data for field in ('instance', 'name')):
                if DoctorDocument.objects.filter(
                    instance=doctor_instance,
                    name=document_name,
                    is_active=True
                ).exclude(id=instance.id).exists():
                    return self.error_response(
                        msg="This document already exists for the doctor",
                        errors={"name": ["Document with this name already exists for this doctor"]},
                        code=status.HTTP_409_CONFLICT
                    )

            document = serializer.save()
            return self.success_response(
                data=self.get_serializer(document).data,
                msg="Doctor document updated successfully"
            )

        return self.error_response(
            msg="Validation failed",
            errors=serializer.errors
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.success_response()
    

class DoctorLanguageViewSet(BaseViewSet):
    queryset = DoctorLanguage.objects.all()
    serializer_class = ser.DoctorLanguageSerializer
    permission_classes = [IsAuthenticated]
    swagger_model = DoctorLanguage
    swagger_model_name = "Doctor Languages"
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = DoctorLanguage.objects.select_related('doctor', 'doctor__user')

        params = self.request.query_params
        doctor_id = params.get('doctor_id')
        language_code = params.get('language_code')
        proficiency_level = params.get('proficiency_level')

        if not self.request.user.is_superuser:
            queryset = queryset.filter(doctor__user=self.request.user)

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        if language_code:
            queryset = queryset.filter(language_code__iexact=language_code)
        
        if proficiency_level:
            queryset = queryset.filter(proficiency_level__icontains=proficiency_level)
        
        queryset = self.apply_search(queryset)
        queryset = self.apply_ordering(queryset)

        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
      
    def create(self, request, *args, **kwargs):
        try:
            doctor = get_object_or_404(Doctor, user=request.user, is_active=True)
            data = request.data.copy()
            data['doctor'] = doctor.id

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)

            if DoctorLanguage.objects.filter(
                doctor=doctor, 
                language_code=serializer.validated_data['language_code']
            ).exists():
                
                return self.error_response(
                    message="Validation failed",
                    errors={"language_code": ["This language already exists for the doctor"]},
                    code=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(doctor=doctor)
            return self.success_response(
                data=serializer.data,
                message="Doctor language created successfully",
                code=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return self.error_response(
                message="Validation failed",
                errors=e.detail if hasattr(e, 'detail') else {"detail": [str(e)]},
                code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.handle_exception(e)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()

            if not request.user.is_superuser and instance.doctor.user != request.user:
                return self.error_response(
                    message="Permission denied",
                    code=status.HTTP_403_FORBIDDEN
                )

            data = request.data.copy()
            data['doctor'] = instance.doctor.id  

            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)

            language_code = serializer.validated_data.get('language_code', instance.language_code)
            if DoctorLanguage.objects.filter(
                doctor=instance.doctor,
                language_code=language_code
            ).exclude(id=instance.id).exists():
                return self.error_response(
                    message="Validation failed",
                    errors={"language_code": ["This language already exists for the doctor"]},
                    code=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return self.success_response(
                data=serializer.data,
                message="Doctor language updated successfully"
            )

        except ValidationError as e:
            return self.error_response(
                message="Validation failed",
                errors=e.detail if hasattr(e, 'detail') else {"detail": [str(e)]},
                code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.handle_exception(e)
        
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.success_response()


class DoctorCertificateViewSet(BaseViewSet):
    queryset = DoctorCertificate.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ser.DoctorCertificateSerializer

    swagger_model = DoctorCertificate
    swagger_model_name = "Doctor Certificates"

    def get_queryset(self):
        queryset = DoctorCertificate.objects.select_related(
            'doctor', 'doctor__user', 'verified_by'
        )

        params = self.request.query_params
        doctor_id = params.get('doctor_id')
        certificate_type = params.get('certificate_type')
        title = params.get('title')
        issuing_organization = params.get('issuing_organization')
        is_verified = params.get('is_verified')
        is_active = params.get('is_active')

        if not self.request.user.is_superuser:
            queryset = queryset.filter(doctor__user=self.request.user)

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        if certificate_type:
            queryset = queryset.filter(certificate_type__icontains=certificate_type)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if issuing_organization:
            queryset = queryset.filter(issuing_organization__icontains=issuing_organization)
        if is_verified is not None:
            queryset = queryset.filter(is_verified=(is_verified.lower() == "true"))
        if is_active is not None:
            queryset = queryset.filter(is_active=(is_active.lower() == "true"))

        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.success_response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, user=request.user, is_active=True)

        data = request.data.copy()
        data['doctor'] = doctor.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if DoctorCertificate.objects.filter(
            doctor=doctor,
            title=serializer.validated_data.get('title'),
            issuing_organization=serializer.validated_data.get('issuing_organization')
        ).exists():
            return self.error_response(
                msg="This certificate already exists for the doctor",
                errors={"title": ["Certificate already exists for this doctor"]},
                code=status.HTTP_400_BAD_REQUEST
            )

        certificate = serializer.save(doctor=doctor)
        return self.success_response(
            data=self.get_serializer(certificate).data,
            code=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            doctor_id = serializer.validated_data.get('doctor')
            title = serializer.validated_data.get('title')
            issuing_organization = serializer.validated_data.get('issuing_organization')

            if doctor_id:
                get_object_or_404(Doctor, id=doctor_id.id, is_active=True)

            if doctor_id and title and issuing_organization:
                if DoctorCertificate.objects.filter(
                    doctor=doctor_id,
                    title=title,
                    issuing_organization=issuing_organization
                ).exclude(id=instance.id).exists():
                    return self.error_response(
                        msg="This certificate already exists for the doctor",
                        errors={"title": ["Certificate already exists for this doctor"]},
                        code=status.HTTP_409_CONFLICT
                    )

            certificate = serializer.save()
            return self.success_response(
                data=self.get_serializer(certificate).data,
            )

        return self.error_response(
            msg="Validation failed",
            errors=serializer.errors
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            doctor_id = serializer.validated_data.get('doctor', instance.doctor)
            title = serializer.validated_data.get('title', instance.title)
            issuing_organization = serializer.validated_data.get(
                'issuing_organization', instance.issuing_organization
            )

            if 'doctor' in serializer.validated_data:
                get_object_or_404(Doctor, id=doctor_id.id, is_active=True)

            if any(field in serializer.validated_data for field in ('doctor', 'title', 'issuing_organization')):
                if DoctorCertificate.objects.filter(
                    doctor=doctor_id,
                    title=title,
                    issuing_organization=issuing_organization
                ).exclude(id=instance.id).exists():
                    return self.error_response(
                        msg="This certificate already exists for the doctor",
                        errors={"title": ["Certificate already exists for this doctor"]},
                        code=status.HTTP_409_CONFLICT
                    )

            certificate = serializer.save()
            return self.success_response(
                data=self.get_serializer(certificate).data,
            )

        return self.error_response(
            msg="Validation failed",
            errors=serializer.errors
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.success_response()


class DoctorEducationViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ser.DoctorEducationSerializer
    swagger_model = DoctorEducation
    swagger_model_name = "Doctor Education"

    def get_queryset(self):
        params = self.request.query_params
        doctor_id = params.get("doctor_id")

        queryset = DoctorEducation.objects.select_related(
            "doctor", "doctor__user"
        )

        if not self.request.user.is_superuser:
            queryset = queryset.filter(instance__user=self.request.user)

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)

        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.validated_data.get("doctor")
            get_object_or_404(Doctor, id=doctor.id, is_active=True)

            if DoctorEducation.objects.filter(
                doctor=doctor,
                degree=serializer.validated_data["degree"],
                institution_name=serializer.validated_data["institution_name"]
            ).exists():
                return self.error_response(
                    msg="This education record already exists for the doctor",
                    errors={"degree": ["Duplicate entry for this doctor and institution"]},
                    code=status.HTTP_409_CONFLICT
                )

            education = serializer.save()
            return self.success_response(
                data=self.get_serializer(education).data,
                msg="Doctor education added successfully",
                code=status.HTTP_201_CREATED
            )

        return self.error_response(msg="Validation failed", errors=serializer.errors)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            doctor = serializer.validated_data.get("doctor", instance.doctor)
            get_object_or_404(Doctor, id=doctor.id, is_active=True)

            if DoctorEducation.objects.filter(
                doctor=doctor,
                degree=serializer.validated_data["degree"],
                institution_name=serializer.validated_data["institution_name"]
            ).exclude(id=instance.id).exists():
                return self.error_response(
                    msg="This education record already exists for the doctor",
                    errors={"degree": ["Duplicate entry for this doctor and institution"]},
                    code=status.HTTP_409_CONFLICT
                )

            education = serializer.save()
            return self.success_response(
                data=self.get_serializer(education).data,
                msg="Doctor education updated successfully"
            )

        return self.error_response(msg="Validation failed", errors=serializer.errors)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            doctor = serializer.validated_data.get("doctor", instance.doctor)
            get_object_or_404(Doctor, id=doctor.id, is_active=True)

            if any(f in serializer.validated_data for f in ("doctor", "degree", "institution_name")):
                if DoctorEducation.objects.filter(
                    doctor=doctor,
                    degree=serializer.validated_data.get("degree", instance.degree),
                    institution_name=serializer.validated_data.get("institution_name", instance.institution_name)
                ).exclude(id=instance.id).exists():
                    return self.error_response(
                        msg="This education record already exists for the doctor",
                        errors={"degree": ["Duplicate entry for this doctor and institution"]},
                        code=status.HTTP_409_CONFLICT
                    )

            education = serializer.save()
            return self.success_response(
                data=self.get_serializer(education).data,
                msg="Doctor education updated successfully"
            )

        return self.error_response(msg="Validation failed", errors=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.success_response()


class DoctorExperienceViewSet(BaseViewSet):
    queryset = DoctorExperience.objects.all()
    serializer_class = ser.DoctorExperienceSerializer
    permission_classes = [IsAuthenticated]
    swagger_model = DoctorExperience
    swagger_model_name = "Doctor Experiences"
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = DoctorExperience.objects.select_related('doctor', 'doctor__user')

        params = self.request.query_params
        doctor_id = params.get('doctor_id')
        position = params.get('position')
        organization_name = params.get('organization_name')
        is_current = params.get('is_current')

        if not self.request.user.is_superuser:
            queryset = queryset.filter(doctor__user=self.request.user)

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        if position:
            queryset = queryset.filter(position__icontains=position)
        
        if organization_name:
            queryset = queryset.filter(organization_name__icontains=organization_name)
        
        if is_current is not None:
            queryset = queryset.filter(is_current=is_current.lower() == 'true')

        queryset = self.apply_search(queryset)
        queryset = self.apply_ordering(queryset)

        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, user=request.user, is_active=True)

        data = request.data.copy()
        data["doctor"] = doctor.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if DoctorExperience.objects.filter(
            doctor=doctor,
            position=serializer.validated_data["position"],
            organization_name=serializer.validated_data["organization_name"],
            start_date=serializer.validated_data["start_date"]
        ).exists():
            raise ValidationError({
                "non_field_errors": ["This experience already exists for the doctor"]
            })

        serializer.save(doctor=doctor)
        return self.success_response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        doctor = get_object_or_404(Doctor, user=request.user, is_active=True)
        
        validated_data = request.data.copy()
        validated_data["doctor"] = doctor.id 

        position = validated_data.get('position', instance.position)
        organization_name = validated_data.get('organization_name', instance.organization_name)
        start_date = validated_data.get('start_date', instance.start_date)

        if DoctorExperience.objects.filter(
            doctor=doctor,
            position=position,
            organization_name=organization_name,
            start_date=start_date
        ).exclude(id=instance.id).exists():
            raise ValidationError({
                "non_field_errors": ["This experience already exists for the doctor"]
            })

        serializer = self.get_serializer(instance, data=validated_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.success_response(serializer.data)

    def partial_update(self, instance, validated_data):
        doctor = validated_data.get('doctor', instance.doctor)
        position = validated_data.get('position', instance.position)
        organization_name = validated_data.get('organization_name', instance.organization_name)
        start_date = validated_data.get('start_date', instance.start_date)

        if 'doctor' in validated_data:
            get_object_or_404(Doctor, id=doctor.id, is_active=True)

        if DoctorExperience.objects.filter(
            doctor=doctor,
            position=position,
            organization_name=organization_name,
            start_date=start_date
        ).exclude(id=instance.id).exists():
            raise ValidationError({
                "non_field_errors": ["This experience already exists for the doctor"]
            })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.success_response()


class DoctorServiceViewSet(BaseViewSet):
    queryset = DoctorService.objects.all()
    serializer_class = ser.DoctorServiceSerializer
    permission_classes = [IsAuthenticated]
    swagger_model = DoctorService
    swagger_model_name = "Doctor Services"
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = DoctorService.objects.select_related('doctor', 'doctor__user')

        params = self.request.query_params
        doctor_id = params.get('doctor_id')
        service_name = params.get('service_name')
        is_active = params.get('is_active')

        if not self.request.user.is_superuser:
            queryset = queryset.filter(doctor__user=self.request.user)

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        if service_name:
            queryset = queryset.filter(service_name__icontains=service_name)
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        queryset = self.apply_search(queryset)
        queryset = self.apply_ordering(queryset)

        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, user=request.user, is_active=True)

        data = request.data.copy()
        data["doctor"] = doctor.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if DoctorService.objects.filter(
            doctor=doctor,
            service_name=serializer.validated_data["service_name"]
        ).exists():
            raise ValidationError({
                "service_name": ["This service already exists for the doctor"]
            })

        serializer.save()
        return self.success_response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        doctor = get_object_or_404(Doctor, user=request.user, is_active=True)

        validated_data = request.data.copy()
        validated_data["doctor"] = doctor.id
        service_name = validated_data.get("service_name", instance.service_name)

        if DoctorService.objects.filter(
            doctor=doctor,
            service_name=service_name
        ).exclude(id=instance.id).exists():
            raise ValidationError({
                "service_name": ["This service already exists for the doctor"]
            })

        serializer = self.get_serializer(instance, data=validated_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.success_response(serializer.data)

    def partial_update(self, instance, validated_data):
        doctor = validated_data.get('doctor', instance.doctor)
        service_name = validated_data.get('service_name', instance.service_name)

        if 'doctor' in validated_data:
            get_object_or_404(Doctor, id=doctor.id, is_active=True)

        if DoctorService.objects.filter(
            doctor=doctor,
            service_name=service_name
        ).exclude(id=instance.id).exists():
            raise ValidationError({
                "service_name": ["This service already exists for the doctor"]
            })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.success_response()


class DoctorSocialMediaViewSet(BaseViewSet):
    queryset = DoctorSocialMedia.objects.all()
    serializer_class = ser.DoctorSocialMediaSerializer
    permission_classes = [IsAuthenticated]
    swagger_model = DoctorSocialMedia
    swagger_model_name = "Doctor Social Media"
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        params = self.request.query_params
        doctor_id = params.get('doctor_id')
        platform = params.get('platform')

        if not self.request.user.is_superuser:
            queryset = queryset.filter(doctor__user=self.request.user)

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        if platform:
            queryset = queryset.filter(platform__icontains=platform)
        
        queryset = self.apply_search(queryset)
        queryset = self.apply_ordering(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, user=request.user, is_active=True)

        data = request.data.copy()
        data['doctor'] = doctor.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if DoctorSocialMedia.objects.filter(
            doctor=doctor,
            platform=serializer.validated_data['platform']
        ).exists():
            raise ValidationError({
                "platform": ["This platform link already exists for the doctor"]
            })

        serializer.save(doctor=doctor)
        return self.success_response(serializer.data)

    def update(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, user=request.user, is_active=True)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data.copy()
        data['doctor'] = doctor.id

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        platform = serializer.validated_data.get('platform', instance.platform)
        if DoctorSocialMedia.objects.filter(
            doctor=doctor,
            platform=platform
        ).exclude(id=instance.id).exists():
            raise ValidationError({
                "platform": ["This platform link already exists for the doctor"]
            })

        serializer.save(doctor=doctor)
        return self.success_response(serializer.data)

    def partial_update(self, instance, validated_data):
        doctor = validated_data.get('doctor', instance.doctor)
        platform = validated_data.get('platform', instance.platform)

        if 'doctor' in validated_data:
            get_object_or_404(Doctor, id=doctor.id, is_active=True)

        if DoctorSocialMedia.objects.filter(
            doctor=doctor,
            platform=platform
        ).exclude(id=instance.id).exists():
            raise ValidationError({
                "platform": ["This platform link already exists for the doctor"]
            })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.success_response()
    

class ClinicSocialMediaViewSet(BaseViewSet):
    queryset = ClinicSocialMedia.objects.all()
    serializer_class = ser.ClinicSocialMediaSerializer
    permission_classes = [IsAuthenticated]
    swagger_model = ClinicSocialMedia
    swagger_model_name = "Clinic Social Media"
    ordering = ['-created_at'] 

    def get_queryset(self):
        queryset = super().get_queryset()

        params = self.request.query_params
        clinic_id = params.get('clinic_id')
        platform = params.get('platform')

        if not self.request.user.is_superuser:
            queryset = queryset.filter(clinic__user=self.request.user)

        if clinic_id:
            queryset = queryset.filter(clinic_id=clinic_id)
        
        if platform:
            queryset = queryset.filter(platform__icontains=platform)
        
        queryset = self.apply_search(queryset)
        queryset = self.apply_ordering(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        clinic = get_object_or_404(Clinic, user=request.user)

        data = request.data.copy()
        data["clinic"] = clinic.id  

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        platform = serializer.validated_data["platform"]
        if ClinicSocialMedia.objects.filter(clinic=clinic, platform=platform).exists():
            return self.error_response(
                msg="This platform link already exists for the clinic",
                errors={"platform": ["This platform link already exists for the clinic"]},
                code=status.HTTP_400_BAD_REQUEST
            )

        social_media = serializer.save(clinic=clinic)
        return self.success_response(
            data=self.get_serializer(social_media).data,
            code=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        clinic = get_object_or_404(Clinic, user=request.user, is_active=True)

        data = request.data.copy()
        data["clinic"] = clinic.id
        platform = data.get('platform', instance.platform)

        if ClinicSocialMedia.objects.filter(
            clinic=clinic,
            platform=platform
        ).exclude(id=instance.id).exists():
            raise ValidationError({
                "platform": ["This platform link already exists for the clinic"]
            })

        serializer = self.get_serializer(instance, data=data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return self.success_response(serializer.data)

    def partial_update(self, instance, validated_data):
        clinic = validated_data.get('clinic', instance.clinic)
        platform = validated_data.get('platform', instance.platform)

        if 'clinic' in validated_data:
            get_object_or_404(Clinic, id=clinic.id, is_active=True)

        if ClinicSocialMedia.objects.filter(
            clinic=clinic,
            platform=platform
        ).exclude(id=instance.id).exists():
            raise ValidationError({
                "platform": ["This platform link already exists for the clinic"]
            })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.success_response()


class DoctorWorkingHourViewSet(BaseViewSet):
    queryset = DoctorWorkingHour.objects.all()
    serializer_class = ser.DoctorWorkingHourSerializer
    permission_classes = [IsAuthenticated]
    swagger_model = DoctorWorkingHour
    swagger_model_name = "Doctor Working Hours"
    ordering = ['-created_at'] 

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        doctor_id = params.get('doctor_id')
        day_of_week = params.get('day_of_week')

        if not self.request.user.is_superuser:
            queryset = queryset.filter(doctor__user=self.request.user)

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)

        if day_of_week:
            queryset = queryset.filter(day_of_week=day_of_week)

        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        day_of_week = request.data.get('day_of_week')

        doctor = get_object_or_404(Doctor, user=request.user)

        if DoctorWorkingHour.objects.filter(
            doctor=doctor,
            day_of_week=day_of_week
        ).exists():
            raise ValidationError({
                "day_of_week": [
                    "Working hours for this day already exist for the doctor."
                ]
            })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(doctor=doctor)

        return self.success_response(serializer.data, code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        doctor = get_object_or_404(Doctor, user=request.user, is_active=True)
        day_of_week = request.data.get('day_of_week', instance.day_of_week)

        if DoctorWorkingHour.objects.filter(
            doctor=doctor, day_of_week=day_of_week
        ).exclude(id=instance.id).exists():
            raise ValidationError({
                "day_of_week": ["Working hours for this day already exist for the doctor."]
            })

        data = request.data.copy()
        data["doctor"] = doctor.id 

        serializer = self.get_serializer(instance, data=data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return self.success_response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.success_response()


class ClinicWorkingHourViewSet(BaseViewSet):
    queryset = ClinicWorkingHour.objects.all()
    serializer_class = ser.ClinicWorkingHourSerializer
    swagger_model = ClinicWorkingHour
    swagger_model_name = "Clinic Working Hours"
    ordering = ['-created_at'] 

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        clinic_id = params.get('clinic_id')
        day_of_week = params.get('day_of_week')

        if not self.request.user.is_superuser:
            queryset = queryset.filter(clinic__user=self.request.user)

        if clinic_id:
            queryset = queryset.filter(clinic_id=clinic_id)

        if day_of_week:
            queryset = queryset.filter(day_of_week=day_of_week)

        return queryset
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        day_of_week = request.data.get('day_of_week')
        clinic = get_object_or_404(Clinic, user=request.user, is_active=True)

        if ClinicWorkingHour.objects.filter(clinic=clinic, day_of_week=day_of_week).exists():
            raise ValidationError({
                "day_of_week": ["Working hours for this day already exist for the clinic."]
            })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(clinic=clinic)  

        return self.success_response(serializer.data, code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        clinic = get_object_or_404(Clinic, user=request.user, is_active=True)
        day_of_week = request.data.get('day_of_week', instance.day_of_week)

        if ClinicWorkingHour.objects.filter(
            clinic=clinic, day_of_week=day_of_week
        ).exclude(id=instance.id).exists():
            raise ValidationError({
                "day_of_week": ["Working hours for this day already exist for the clinic."]
            })

        data = request.data.copy()
        data["clinic"] = clinic.id 

        serializer = self.get_serializer(instance, data=data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return self.success_response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.success_response()


class ReviewViewSet(BaseViewSet):
    queryset = Review.objects.all()
    serializer_class = ser.ReviewSerializer
    swagger_model = Review
    swagger_model_name = "Reviews"
    ordering = ['-created_at'] 

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        clinic_id = params.get('clinic_id')
        doctor_id = params.get('doctor_id')
        patient_id = params.get('patient_id')
        is_verified = params.get('is_verified')
        is_active = params.get('is_active')

        if not self.request.user.is_superuser:
            queryset = queryset.filter(clinic__user=self.request.user)

        if clinic_id:
            queryset = queryset.filter(clinic_id=clinic_id)

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)

        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        if is_verified is not None:
            queryset = queryset.filter(is_verified=is_verified.lower() in ["true", "1"])

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() in ["true", "1"])

        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        clinic_id = request.data.get('clinic')
        doctor_id = request.data.get('doctor')
        patient_id = request.data.get('patient')

        clinic = get_object_or_404(Clinic, id=clinic_id, is_active=True)
        doctor = get_object_or_404(Doctor, id=doctor_id, is_active=True)
        patient = get_object_or_404(Patient, id=patient_id, is_active=True)

        if Review.objects.filter(
            clinic=clinic, doctor=doctor, patient=patient
        ).exists():
            raise ValidationError({
                "non_field_errors": [
                    "This patient has already submitted a review for this doctor in this clinic."
                ]
            })

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        clinic_id = request.data.get('clinic', instance.clinic.id)
        doctor_id = request.data.get('doctor', instance.doctor.id)
        patient_id = request.data.get('patient', instance.patient.id)

        clinic = get_object_or_404(Clinic, id=clinic_id, is_active=True)
        doctor = get_object_or_404(Doctor, id=doctor_id, is_active=True)
        patient = get_object_or_404(Patient, id=patient_id, is_active=True)

        if Review.objects.filter(
            clinic=clinic, doctor=doctor, patient=patient
        ).exclude(id=instance.id).exists():
            raise ValidationError({
                "non_field_errors": [
                    "This patient has already submitted a review for this doctor in this clinic."
                ]
            })

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.success_response()
    















# @document_upload_schema(
#     model_name='patient',
#     model_display_name='Patient',
#     tag='Patients',
#     additional_fields={
#         'patient': {'type': 'integer', 'description': 'Patient ID'},
#         'document_type': {'type': 'string', 'description': 'Type of patient document', 'example': 'medical_history'}
#     },
#     additional_request_fields={
#         'document_type': {
#             'type': 'string',
#             'description': 'Type of patient document',
#             'example': 'medical_history',
#             'enum': ['medical_history', 'prescription', 'lab_result', 'insurance_card', 'other']
#         }
#     },
#     additional_example_data={
#         'patient': 1,
#         'document_type': 'medical_history'
#     }
# )
# class PatientDocumentUploadView(BaseDocumentView):
#     serializer_class = PatientDocumentSerializer
#     queryset = PatientDocument.objects.all()
#     model = PatientDocument

#     def get_queryset(self):
#         return super().get_queryset().filter(instance__user=self.request.user)