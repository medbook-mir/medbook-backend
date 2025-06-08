import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from medbook.models import MedicalTest

User = get_user_model()

@pytest.mark.django_db
def test_protected_test_list_view():
    pass
    # user = User.objects.create_user(username='testuser', password='testpass')
    # MedicalTest.objects.create(name='Test 1')
    # MedicalTest.objects.create(name='Test 2')

    # client = APIClient()


    # response = client.get('/api/medical-tests/')
    # assert response.status_code in [401, 403]


    # client.force_authenticate(user=user)
    # response = client.get('/api/medical-tests/')
    # assert response.status_code == 200

  
    # assert "data" in response.data, "Ожидался ключ 'data' в ответе"
    # assert isinstance(response.data["data"], list), "Поле 'data' должно быть списком"
    # assert len(response.data["data"]) == 2, "Должно быть 2 теста"

