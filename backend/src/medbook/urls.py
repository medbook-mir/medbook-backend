import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    DecoratedTokenObtainPairView,
    DoctorOrClinicSignupView,
    SendOTPView,
    TestListView,
    VerifyOTPView,
    health_check,
)

SERVICE_TYPE = os.getenv("SERVICE_TYPE", "backend")
common_patterns = [
    path("admin/", admin.site.urls),
    path("api/auth/send/", SendOTPView.as_view(), name="patient_signup"),
    path("api/auth/verify/", VerifyOTPView.as_view(), name="verify_code"),
    path("api/doctor/signup/", DoctorOrClinicSignupView.as_view()),
    path(
        "api/auth/login/",
        DecoratedTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/medical-tests/", TestListView.as_view(), name="medical-tests-list"),
    path("accounts/", include("allauth.urls")),
    path(
        "api/auth/google/",
        RedirectView.as_view(url="/accounts/google/login/"),
        name="google_login",
    ),
    path("ping/", health_check),
]

if SERVICE_TYPE == "api":
    urlpatterns = [
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ] + common_patterns
else:
    urlpatterns = [
        path("", TemplateView.as_view(template_name="index.html")),
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ] + common_patterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
