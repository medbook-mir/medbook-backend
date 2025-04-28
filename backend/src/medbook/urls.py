from os import path
from django.http import JsonResponse

urlpatterns = [
    path('health-check/', lambda r: JsonResponse({'status': 'ok'})),
]