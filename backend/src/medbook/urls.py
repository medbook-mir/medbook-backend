from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
   openapi.Info(
      title="MedBook API",
      default_version='v1',
      description="API for MedBook application",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_endpoint(request):
    return Response({'message': 'This is a public endpoint'})

@api_view(['GET'])
def private_endpoint(request):
    return Response({'message': 'This is a private endpoint'})

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/public/', public_endpoint, name='public-endpoint'),
    path('api/private/', private_endpoint, name='private-endpoint'),
]