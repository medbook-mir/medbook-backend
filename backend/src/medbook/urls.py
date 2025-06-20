import os
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .views import SomeProtectedView, TestListView, SignupView, VerifyCodeView, health_check


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        request=TokenObtainPairSerializer,
        responses={
            200: OpenApiResponse(
                response=dict,
                description="Токены получены"
            ),
            400: OpenApiResponse(description="Неверные учетные данные"),
        },
        description="Получение JWT токена по username и password"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

SERVICE_TYPE = os.getenv('SERVICE_TYPE', 'backend')
common_patterns = [
    path('admin/', admin.site.urls),
    path('api/token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('api/protected-endpoint/', SomeProtectedView.as_view()),
    path('api/medical-tests/', TestListView.as_view(), name='medical-tests-list'),
    path("ping/", health_check),
]

if SERVICE_TYPE == 'api':
    urlpatterns = [
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ] + common_patterns
else:
    urlpatterns = [
        path('', TemplateView.as_view(template_name='index.html')), 
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ] + common_patterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
