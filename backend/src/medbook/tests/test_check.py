import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from medbook.models import MedicalTest

User = get_user_model()

@pytest.mark.django_db
def test_protected_test_list_view():
    # Create user
    user = User.objects.create_user(username='testuser', password='testpass')
    
    # Create test data
    MedicalTest.objects.create(name='Test 1')
    MedicalTest.objects.create(name='Test 2')

    # Authenticate properly
    client = APIClient()
    client.force_authenticate(user=user)  # Changed from client.login()
    
    # Make request
    response = client.get('/medical-test/')
    
    # Assertions
    assert response.status_code == 200
    assert 'data' in response.data
    assert len(response.data['data']) == 2
    assert response.data['message'] == "Это защищенный эндпоинт"