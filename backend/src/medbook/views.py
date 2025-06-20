from django.http import JsonResponse
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from .serializers import SignupSerializer, VerifyCodeSerializer, TestSerializer
from .models import MedicalTest


User = get_user_model()


def health_check(request):
    return JsonResponse({"status": "ok"})


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return response
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Доступ разрешен!"})


class SomeProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Это защищенный эндпоинт"})


class TestListView(generics.ListAPIView):
    queryset = MedicalTest.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Это защищенный эндпоинт",
            "data": serializer.data
        })


class SignupView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=SignupSerializer,
        responses={
            201: OpenApiResponse(
                response=dict,
                description="Verification code sent"
            ),
            400: OpenApiResponse(description="Invalid input"),
        },
        description="Register a new user with required fields. A verification code will be sent to the email.",
        examples=[
            OpenApiExample(
                name="Signup Example",
                value={
                    "username": "john_doe",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john@example.com",
                    "phone_number": "+998901234567",
                    "is_gender": True,
                    "password": "strong_password123"
                },
                request_only=True
            )
        ]
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Verification code sent to email. Check your console for the code."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=VerifyCodeSerializer,
        responses={
            200: OpenApiResponse(
                response=dict,
                description="Verification successful"
            ),
            400: OpenApiResponse(description="Invalid code or input"),
        },
        description="Verify user by submitting the email verification code.",
        examples=[
            OpenApiExample(
                name="Verification Example",
                value={"email_code": "123456"},
                request_only=True
            )
        ]
    )
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            email_code = serializer.validated_data['email_code']
            try:
                user = User.objects.get(email_code=email_code)
                if not user.is_active:
                    user.is_active = True
                    user.email_code = None
                    user.save()
                    return Response({"message": "Verification successful. You can now log in."}, status=status.HTTP_200_OK)
                return Response({"message": "Account already verified."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)