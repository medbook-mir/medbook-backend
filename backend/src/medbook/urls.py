import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView
from .routers import router
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from .views import test_minio, BookingDetailView, PatientProfileImageDetailView

from .views import (
    DecoratedTokenObtainPairView,
    DecoratedTokenRefreshView,
    DoctorOrClinicSignupView,
    PatientProfileView,
    SendOTPView,
    VerifyOTPView,
    health_check,
    UpdatePatientProfileByIdView,
    UploadPatientProfileImageView,
    BookingListView,
    BookingCancelView,
    BookingRescheduleView,
    PatientChatListView,
    PatientChatDetailView,
    SendMessageView,
    PatientMarkChatAsReadView,
)

SERVICE_TYPE = os.getenv("SERVICE_TYPE", "api")
common_patterns = [
    path("admin/", admin.site.urls),
    path("api/auth/send/", SendOTPView.as_view(), name="patient_signup"),
    path("api/auth/verify/", VerifyOTPView.as_view(), name="verify_code"),
    path("api/doctor/signup/", DoctorOrClinicSignupView.as_view()),
    path("api/auth/login/",DecoratedTokenObtainPairView.as_view(),name="token_obtain_pair"),
    path("api/token/refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
    # path("api/medical-tests/", TestListView.as_view(), name="medical-tests-list"),
    path('api/', include(router.urls)),
    path("accounts/", include("allauth.urls")),
    path("api/auth/google/",RedirectView.as_view(url="/accounts/google/login/"),name="google_login"),
    path("test-minio/", test_minio, name="test_minio"),
    path("ping/", health_check),
]

common_patterns += [
    path("api/patient/profile/", PatientProfileView.as_view(), name="patient_profile"),
    path('api/patient/profile/<int:id>/', UpdatePatientProfileByIdView.as_view(), name='update-patient-profile'),
    path('api/patient/profile/image/', UploadPatientProfileImageView.as_view(), name='upload-patient-profile-image'),
    path('api/patient/profile/image/<int:pk>/',PatientProfileImageDetailView.as_view(),name='patient-profile-image-detail'),
    path("api/bookings/", BookingListView.as_view(), name="booking-list"),
    path("api/bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path('api/patient/bookings/<int:booking_id>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
    path('api/patient/bookings/<int:booking_id>/reschedule/', BookingRescheduleView.as_view(), name='booking-reschedule'),
    path("patient/chats/", PatientChatListView.as_view(), name="patient-chat-list"),
    path("patient/chats/<int:chat_id>/", PatientChatDetailView.as_view(), name="patient-chat-detail"),
    path("patient/chats/<int:chat_id>/send/", SendMessageView.as_view(), name="patient-chat-send"),
    path("patient/chats/<int:chat_id>/read/", PatientMarkChatAsReadView.as_view(), name="patient-chat-mark-read"),
]

if SERVICE_TYPE == "api":
    urlpatterns = [
        path("", RedirectView.as_view(url="/swagger/", permanent=False)),
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path("swagger/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui"),
        path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ] + common_patterns
else:
    urlpatterns = [
        path("", TemplateView.as_view(template_name="index.html")),
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path("swagger/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui"),
        path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ] + common_patterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
