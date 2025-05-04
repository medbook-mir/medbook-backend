import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from medbook.models import MedicalTest 

@pytest.mark.django_db
def test_protected_test_list_view():
    user = User.objects.create_user(username='testuser', password='testpass')

    MedicalTest.objects.create(name='Test 1') 
    MedicalTest.objects.create(name='Test 2')

    client = APIClient()
    client.login(username='testuser', password='testpass') 

    response = client.get('/medical-test/')

    assert response.status_code == 200
    assert 'data' in response.data
    assert len(response.data['data']) == 2
    assert response.data['message'] == "Это защищенный эндпоинт"
