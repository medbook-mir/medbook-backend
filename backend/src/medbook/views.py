from django.contrib.auth import get_user_model
from django.http import JsonResponse
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Doctor, MedicalTest
from .serializers import (
    DoctorDetailSerializer,
    DoctorOrClinicSignupSerializer,
    DoctorSerializer,
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


class DoctorPagination(PageNumberPagination):
    """Custom pagination class for doctor listings."""
    
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'


class GetDoctorsView(APIView):
    """API view for retrieving a paginated list of doctors."""
    
    permission_classes = [AllowAny]
    pagination_class = DoctorPagination

    @extend_schema(
        operation_id="get_doctors",
        summary="Get Doctors List API",
        description=(
            "Retrieve a paginated list of all active doctors "
            "with their basic information"
        ),
        parameters=[
            {
                "name": "page",
                "in": "query",
                "description": "Page number for pagination",
                "required": False,
                "type": "integer",
                "default": 1,
            },
            {
                "name": "page_size",
                "in": "query",
                "description": "Number of items per page (max 100)",
                "required": False,
                "type": "integer",
                "default": 10,
            },
            {
                "name": "specialty",
                "in": "query",
                "description": "Filter doctors by specialty ID",
                "required": False,
                "type": "integer",
            },
            {
                "name": "clinic",
                "in": "query",
                "description": "Filter doctors by clinic ID",
                "required": False,
                "type": "integer",
            },
            {
                "name": "is_online",
                "in": "query",
                "description": "Filter doctors by online consultation availability",
                "required": False,
                "type": "boolean",
            },
            {
                "name": "is_primary",
                "in": "query",
                "description": "Filter doctors by primary care status",
                "required": False,
                "type": "boolean",
            },
        ],
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer", "example": 25},
                        "next": {
                            "type": "string",
                            "nullable": True,
                            "example": "http://example.com/api/doctors/?page=2"
                        },
                        "previous": {
                            "type": "string",
                            "nullable": True,
                            "example": None
                        },
                        "results": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/DoctorSerializer"},
                        },
                    },
                },
                description="Paginated list of doctors retrieved successfully",
            ),
            400: OpenApiResponse(description="Invalid query parameters"),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                value={
                    "count": 25,
                    "next": "http://example.com/api/doctors/?page=2",
                    "previous": None,
                    "results": [
                        {
                            "id": 1,
                            "user": {
                                "id": 1,
                                "first_name": "John",
                                "last_name": "Doe",
                                "email": "john.doe@example.com",
                                "phone_number": "+998901234567",
                                "gender": "male",
                                "profile_image_url": "https://example.com/doctor1.jpg",
                                "is_verified": True,
                            },
                            "clinic": {
                                "id": 1,
                                "name": "Health Plus Medical Center",
                                "website_url": "https://healthplus.com",
                                "profile_image_url": "https://example.com/clinic1.jpg",
                                "description": "Leading medical center",
                                "established_year": 2010,
                                "total_staff": 50,
                            },
                            "license_number": "MD123456",
                            "consultation_fee": "50.00",
                            "online_consultation_fee": "30.00",
                            "average_consultation_time": 30,
                            "is_online_consultation_available": True,
                            "rating": "4.8",
                            "total_reviews": 150,
                            "total_patients": 500,
                            "bio": "Experienced cardiologist with 10+ years of practice",
                            "years_of_experience": 10,
                            "specialty": {
                                "id": 1,
                                "name": "Cardiology",
                                "description": "Heart and cardiovascular system",
                                "category": "specialist",
                            },
                            "is_primary": False,
                            "is_active": True,
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": "2024-01-15T10:30:00Z",
                        }
                    ],
                },
                response_only=True,
            )
        ],
        tags=["Doctors"],
    )
    def get(self, request):
        """Handle GET request to retrieve paginated list of doctors."""
        try:
            # Get query parameters for filtering
            specialty_id = request.query_params.get("specialty")
            clinic_id = request.query_params.get("clinic")
            is_online = request.query_params.get("is_online")
            is_primary = request.query_params.get("is_primary")

            # Start with all active doctors
            queryset = Doctor.objects.filter(
                is_active=True, 
                is_deleted__isnull=True
            )

            # Apply filters
            if specialty_id:
                queryset = queryset.filter(specialty_id=specialty_id)
            
            if clinic_id:
                queryset = queryset.filter(clinic_id=clinic_id)
            
            if is_online is not None:
                is_online_bool = is_online.lower() == "true"
                queryset = queryset.filter(
                    is_online_consultation_available=is_online_bool
                )
            
            if is_primary is not None:
                is_primary_bool = is_primary.lower() == "true"
                queryset = queryset.filter(is_primary=is_primary_bool)

            # Order by rating (highest first) and then by name
            queryset = queryset.order_by(
                "-rating", 
                "user__first_name", 
                "user__last_name"
            )

            # Apply pagination
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            
            # Serialize the data
            serializer = DoctorSerializer(paginated_queryset, many=True)
            
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response(
                {"error": f"Error retrieving doctors: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetDoctorByIdView(APIView):
    """API view for retrieving a specific doctor by ID."""
    
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="get_doctor_by_id",
        summary="Get Doctor by ID API",
        description=(
            "Retrieve detailed information about a specific doctor by their ID"
        ),
        parameters=[
            {
                "name": "id",
                "in": "path",
                "description": "Doctor ID",
                "required": True,
                "type": "integer",
            },
        ],
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "user": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "first_name": {"type": "string"},
                                "last_name": {"type": "string"},
                                "email": {"type": "string"},
                                "phone_number": {"type": "string"},
                                "gender": {"type": "string"},
                                "profile_image_url": {"type": "string"},
                                "is_verified": {"type": "boolean"},
                            },
                        },
                        "clinic": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "string"},
                                "website_url": {"type": "string"},
                                "profile_image_url": {"type": "string"},
                                "description": {"type": "string"},
                                "established_year": {"type": "integer"},
                                "total_staff": {"type": "integer"},
                            },
                        },
                        "license_number": {"type": "string"},
                        "consultation_fee": {"type": "string"},
                        "online_consultation_fee": {"type": "string"},
                        "average_consultation_time": {"type": "integer"},
                        "is_online_consultation_available": {"type": "boolean"},
                        "rating": {"type": "string"},
                        "total_reviews": {"type": "integer"},
                        "total_patients": {"type": "integer"},
                        "bio": {"type": "string"},
                        "years_of_experience": {"type": "integer"},
                        "specialty": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                                "category": {"type": "string"},
                            },
                        },
                        "is_primary": {"type": "boolean"},
                        "is_active": {"type": "boolean"},
                        "verified_by": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "first_name": {"type": "string"},
                                "last_name": {"type": "string"},
                            },
                        },
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                    },
                },
                description="Doctor details retrieved successfully",
            ),
            404: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "Doctor not found",
                        },
                    },
                },
                description="Doctor not found",
            ),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                value={
                    "id": 1,
                    "user": {
                        "id": 1,
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "john.doe@example.com",
                        "phone_number": "+998901234567",
                        "gender": "male",
                        "profile_image_url": "https://example.com/doctor1.jpg",
                        "is_verified": True,
                    },
                    "clinic": {
                        "id": 1,
                        "name": "Health Plus Medical Center",
                        "website_url": "https://healthplus.com",
                        "profile_image_url": "https://example.com/clinic1.jpg",
                        "description": "Leading medical center",
                        "established_year": 2010,
                        "total_staff": 50,
                    },
                    "license_number": "MD123456",
                    "consultation_fee": "50.00",
                    "online_consultation_fee": "30.00",
                    "average_consultation_time": 30,
                    "is_online_consultation_available": True,
                    "rating": "4.8",
                    "total_reviews": 150,
                    "total_patients": 500,
                    "bio": (
                        "Experienced cardiologist with 10+ years of practice "
                        "specializing in interventional cardiology and preventive care."
                    ),
                    "years_of_experience": 10,
                    "specialty": {
                        "id": 1,
                        "name": "Cardiology",
                        "description": "Heart and cardiovascular system",
                        "category": "specialist",
                    },
                    "is_primary": False,
                    "is_active": True,
                    "verified_by": {
                        "id": 1,
                        "first_name": "Admin",
                        "last_name": "User",
                    },
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-15T10:30:00Z",
                },
                response_only=True,
            )
        ],
        tags=["Doctors"],
    )
    def get(self, request, doctor_id):
        """Handle GET request to retrieve a specific doctor by ID."""
        try:
            doctor = Doctor.objects.get(
                id=doctor_id, 
                is_active=True, 
                is_deleted__isnull=True
            )
            serializer = DoctorDetailSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Error retrieving doctor: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
