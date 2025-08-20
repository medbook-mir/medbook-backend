# import sys
# import os

# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password
# from django.test import TestCase, override_settings
# from rest_framework import status
# from rest_framework.test import APIClient
# from rest_framework_simplejwt.tokens import RefreshToken

# from medbook.models import Clinic, Doctor, Specialty

# User = get_user_model()


# @override_settings(EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend")
# class DoctorViewsTests(TestCase):
#     """Test cases for GetDoctorsView and GetDoctorByIdView."""

#     def setUp(self):
#         """Set up test data and authentication."""
#         self.client = APIClient()
        
#         # Create test specialty
#         self.specialty = Specialty.objects.create(
#             name="Cardiology",
#             description="Heart and cardiovascular system",
#             category="specialist"
#         )
        
#         # Create test clinic
#         self.clinic = Clinic.objects.create(
#             user=User.objects.create(
#                 username="clinic@example.com",
#                 email="clinic@example.com",
#                 password=make_password("clinicpass123"),
#                 is_active=True,
#                 role="CLINIC"
#             ),
#             name="Health Plus Medical Center",
#             description="Leading medical center",
#             established_year=2010,
#             total_staff=50
#         )
        
#         # Create test doctors
#         self.doctor1 = Doctor.objects.create(
#             user=User.objects.create(
#                 username="doctor1@example.com",
#                 email="doctor1@example.com",
#                 first_name="John",
#                 last_name="Doe",
#                 password=make_password("doctorpass123"),
#                 is_active=True,
#                 is_verified=True,
#                 role="DOCTOR"
#             ),
#             clinic=self.clinic,
#             license_number="MD123456",
#             consultation_fee=50.00,
#             online_consultation_fee=30.00,
#             average_consultation_time=30,
#             is_online_consultation_available=True,
#             rating=4.8,
#             total_reviews=150,
#             total_patients=500,
#             bio="Experienced cardiologist with 10+ years of practice",
#             years_of_experience=10,
#             specialty=self.specialty,
#             is_primary=False,
#             is_active=True
#         )
        
#         self.doctor2 = Doctor.objects.create(
#             user=User.objects.create(
#                 username="doctor2@example.com",
#                 email="doctor2@example.com",
#                 first_name="Jane",
#                 last_name="Smith",
#                 password=make_password("doctorpass456"),
#                 is_active=True,
#                 is_verified=True,
#                 role="DOCTOR"
#             ),
#             clinic=self.clinic,
#             license_number="MD789012",
#             consultation_fee=60.00,
#             online_consultation_fee=40.00,
#             average_consultation_time=45,
#             is_online_consultation_available=False,
#             rating=4.5,
#             total_reviews=100,
#             total_patients=300,
#             bio="General practitioner with 5 years of experience",
#             years_of_experience=5,
#             specialty=self.specialty,
#             is_primary=True,
#             is_active=True
#         )

#     def test_get_doctors_list_success(self):
#         """Test successful retrieval of doctors list without authentication."""
#         response = self.client.get("/api/doctors/")
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("count", response.data)
#         self.assertIn("next", response.data)
#         self.assertIn("previous", response.data)
#         self.assertIn("results", response.data)
        
#         # Check that we have 2 doctors
#         self.assertEqual(response.data["count"], 2)
        
#         # Check results structure
#         results = response.data["results"]
#         self.assertEqual(len(results), 2)
        
#         # Check first doctor data
#         doctor1_data = results[0]  # Should be doctor1 due to higher rating
#         self.assertEqual(doctor1_data["id"], self.doctor1.id)
#         self.assertEqual(doctor1_data["license_number"], "MD123456")
#         # Handle decimal formatting - convert to float for comparison
#         self.assertEqual(float(doctor1_data["rating"]), 4.8)
#         self.assertTrue(doctor1_data["is_online_consultation_available"])
        
#         # Check nested user data
#         self.assertEqual(doctor1_data["user"]["first_name"], "John")
#         self.assertEqual(doctor1_data["user"]["last_name"], "Doe")
#         self.assertEqual(doctor1_data["user"]["email"], "doctor1@example.com")
        
#         # Check nested clinic data
#         self.assertEqual(doctor1_data["clinic"]["name"], "Health Plus Medical Center")
#         self.assertEqual(doctor1_data["clinic"]["established_year"], 2010)
        
#         # Check nested specialty data
#         self.assertEqual(doctor1_data["specialty"]["name"], "Cardiology")
#         self.assertEqual(doctor1_data["specialty"]["category"], "specialist")

#     def test_get_doctors_list_with_pagination(self):
#         """Test doctors list with pagination parameters."""
#         response = self.client.get("/api/doctors/?page=1&page_size=1")
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["count"], 2)
#         self.assertEqual(len(response.data["results"]), 1)
#         self.assertIsNotNone(response.data["next"])
#         self.assertIsNone(response.data["previous"])

#     def test_get_doctors_list_filter_by_specialty(self):
#         """Test filtering doctors by specialty."""
#         response = self.client.get(f"/api/doctors/?specialty={self.specialty.id}")
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["count"], 2)
        
#         # All returned doctors should have the same specialty
#         for doctor in response.data["results"]:
#             self.assertEqual(doctor["specialty"]["id"], self.specialty.id)

#     def test_get_doctors_list_filter_by_clinic(self):
#         """Test filtering doctors by clinic."""
#         response = self.client.get(f"/api/doctors/?clinic={self.clinic.id}")
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["count"], 2)
        
#         # All returned doctors should belong to the same clinic
#         for doctor in response.data["results"]:
#             self.assertEqual(doctor["clinic"]["id"], self.clinic.id)

#     def test_get_doctors_list_filter_by_online_consultation(self):
#         """Test filtering doctors by online consultation availability."""
#         response = self.client.get("/api/doctors/?is_online=true")
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         # Only doctors with online consultation should be returned
#         for doctor in response.data["results"]:
#             self.assertTrue(doctor["is_online_consultation_available"])

#     def test_get_doctors_list_filter_by_primary_care(self):
#         """Test filtering doctors by primary care status."""
#         response = self.client.get("/api/doctors/?is_primary=true")
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         # Only primary care doctors should be returned
#         for doctor in response.data["results"]:
#             self.assertTrue(doctor["is_primary"])

#     def test_get_doctor_by_id_success(self):
#         """Test successful retrieval of a specific doctor without authentication."""
#         response = self.client.get(f"/api/doctors/{self.doctor1.id}/")
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         # Check doctor data
#         doctor_data = response.data
#         self.assertEqual(doctor_data["id"], self.doctor1.id)
#         self.assertEqual(doctor_data["license_number"], "MD123456")
#         self.assertEqual(doctor_data["consultation_fee"], "50.00")
#         self.assertEqual(doctor_data["online_consultation_fee"], "30.00")
#         self.assertEqual(doctor_data["average_consultation_time"], 30)
#         self.assertTrue(doctor_data["is_online_consultation_available"])
#         # Handle decimal formatting - convert to float for comparison
#         self.assertEqual(float(doctor_data["rating"]), 4.8)
#         self.assertEqual(doctor_data["total_reviews"], 150)
#         self.assertEqual(doctor_data["total_patients"], 500)
#         self.assertEqual(doctor_data["bio"], "Experienced cardiologist with 10+ years of practice")
#         self.assertEqual(doctor_data["years_of_experience"], 10)
#         self.assertFalse(doctor_data["is_primary"])
#         self.assertTrue(doctor_data["is_active"])
        
#         # Check nested user data
#         self.assertEqual(doctor_data["user"]["id"], self.doctor1.user.id)
#         self.assertEqual(doctor_data["user"]["first_name"], "John")
#         self.assertEqual(doctor_data["user"]["last_name"], "Doe")
#         self.assertEqual(doctor_data["user"]["email"], "doctor1@example.com")
#         self.assertTrue(doctor_data["user"]["is_verified"])
        
#         # Check nested clinic data
#         self.assertEqual(doctor_data["clinic"]["id"], self.clinic.id)
#         self.assertEqual(doctor_data["clinic"]["name"], "Health Plus Medical Center")
#         self.assertEqual(doctor_data["clinic"]["description"], "Leading medical center")
#         self.assertEqual(doctor_data["clinic"]["established_year"], 2010)
#         self.assertEqual(doctor_data["clinic"]["total_staff"], 50)
        
#         # Check nested specialty data
#         self.assertEqual(doctor_data["specialty"]["id"], self.specialty.id)
#         self.assertEqual(doctor_data["specialty"]["name"], "Cardiology")
#         self.assertEqual(doctor_data["specialty"]["description"], "Heart and cardiovascular system")
#         self.assertEqual(doctor_data["specialty"]["category"], "specialist")

#     def test_get_doctor_by_id_not_found(self):
#         """Test retrieval of non-existent doctor."""
#         response = self.client.get("/api/doctors/999/")
        
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data["error"], "Doctor not found")

#     def test_get_inactive_doctor_by_id(self):
#         """Test that inactive doctors are not returned."""
#         # Deactivate a doctor
#         self.doctor1.is_active = False
#         self.doctor1.save()
        
#         response = self.client.get(f"/api/doctors/{self.doctor1.id}/")
        
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data["error"], "Doctor not found")

#     def test_get_doctors_list_excludes_inactive(self):
#         """Test that inactive doctors are excluded from the list."""
#         # Deactivate a doctor
#         self.doctor1.is_active = False
#         self.doctor1.save()
        
#         response = self.client.get("/api/doctors/")
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["count"], 1)  # Only active doctor should be returned
        
#         # Check that only the active doctor is in results
#         doctor_ids = [doctor["id"] for doctor in response.data["results"]]
#         self.assertNotIn(self.doctor1.id, doctor_ids)
#         self.assertIn(self.doctor2.id, doctor_ids)

#     def test_get_doctors_list_ordering(self):
#         """Test that doctors are ordered by rating (highest first) then by name."""
#         response = self.client.get("/api/doctors/")
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         results = response.data["results"]
#         self.assertEqual(len(results), 2)
        
#         # First doctor should have higher rating (4.8 > 4.5)
#         self.assertEqual(float(results[0]["rating"]), 4.8)
#         self.assertEqual(float(results[1]["rating"]), 4.5)

#     def test_get_doctors_list_multiple_filters(self):
#         """Test combining multiple filters."""
#         response = self.client.get(
#             f"/api/doctors/?specialty={self.specialty.id}&clinic={self.clinic.id}&is_online=true"
#         )
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         # All returned doctors should match all filter criteria
#         for doctor in response.data["results"]:
#             self.assertEqual(doctor["specialty"]["id"], self.specialty.id)
#             self.assertEqual(doctor["clinic"]["id"], self.clinic.id)
#             self.assertTrue(doctor["is_online_consultation_available"])

#     def test_get_doctors_list_invalid_page_size(self):
#         """Test handling of invalid page size."""
#         response = self.client.get("/api/doctors/?page_size=1000")  # Exceeds max_page_size
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # Should default to max_page_size (100)
#         self.assertLessEqual(len(response.data["results"]), 100)

#     def test_get_doctors_empty_list(self):
#         """Test behavior when no doctors exist."""
#         # Remove all doctors
#         Doctor.objects.all().delete()

#         response = self.client.get("/api/doctors/")

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["count"], 0)
#         self.assertEqual(len(response.data["results"]), 0)

#     def test_get_doctors_list_filter_no_results(self):
#         """Test filtering that returns no results."""
#         # Create a new specialty that no doctor has
#         new_specialty = Specialty.objects.create(
#             name="Test Specialty",
#             description="Test specialty",
#             category="specialist"
#         )

#         response = self.client.get(f"/api/doctors/?specialty={new_specialty.id}")

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["count"], 0)
#         self.assertEqual(len(response.data["results"]), 0)


# # Example usage and testing instructions
# """
# HOW TO TEST THE DOCTOR VIEWS:

# 1. **Setup and Run Tests:**
#    ```bash
#    cd backend/src
#    python manage.py test medbook.tests.test_doctors
#    ```

# 2. **Manual Testing with curl (No Authentication Required):**

#    **Get Doctors List:**
#    ```bash
#    # Get all doctors
#    curl http://localhost:8000/api/doctors/
   
#    # With pagination
#    curl "http://localhost:8000/api/doctors/?page=1&page_size=10"
   
#    # With filters
#    curl "http://localhost:8000/api/doctors/?specialty=1&is_online=true"
#    ```

#    **Get Doctor by ID:**
#    ```bash
#    curl http://localhost:8000/api/doctors/1/
#    ```

# 3. **Testing with Python requests:**
#    ```python
#    import requests
   
#    # Test GetDoctorsView (no authentication needed)
#    response = requests.get('http://localhost:8000/api/doctors/')
#    print(response.json())
   
#    # Test GetDoctorByIdView (no authentication needed)
#    response = requests.get('http://localhost:8000/api/doctors/1/')
#    print(response.json())
#    ```

# 4. **Testing with Postman:**
#    - No authentication headers needed
#    - GET http://localhost:8000/api/doctors/
#    - GET http://localhost:8000/api/doctors/1/
#    - Add query parameters for filtering

# 5. **Expected Response Examples:**

#    **GetDoctorsView Response:**
#    ```json
#    {
#      "count": 2,
#      "next": null,
#      "previous": null,
#      "results": [
#        {
#          "id": 1,
#          "user": {
#            "id": 2,
#            "first_name": "John",
#            "last_name": "Doe",
#            "email": "doctor1@example.com",
#            "phone_number": null,
#            "gender": null,
#            "profile_image_url": null,
#            "is_verified": true
#          },
#          "clinic": {
#            "id": 1,
#            "name": "Health Plus Medical Center",
#            "website_url": null,
#            "profile_image_url": null,
#            "description": "Leading medical center",
#            "established_year": 2010,
#            "total_staff": 50
#          },
#          "license_number": "MD123456",
#          "consultation_fee": "50.00",
#          "online_consultation_fee": "30.00",
#          "average_consultation_time": 30,
#          "is_online_consultation_available": true,
#          "rating": "4.80",
#          "total_reviews": 150,
#          "total_patients": 500,
#          "bio": "Experienced cardiologist with 10+ years of practice",
#          "years_of_experience": 10,
#          "specialty": {
#            "id": 1,
#            "name": "Cardiology",
#            "description": "Heart and cardiovascular system",
#            "category": "specialist"
#          },
#          "is_primary": false,
#          "is_active": true,
#          "created_at": "2024-01-15T10:30:00Z",
#          "updated_at": "2024-01-15T10:30:00Z"
#        }
#      ]
#    }
#    ```

#    **GetDoctorByIdView Response:**
#    ```json
#    {
#      "id": 1,
#      "user": {
#        "id": 2,
#        "first_name": "John",
#        "last_name": "Doe",
#        "email": "doctor1@example.com",
#        "phone_number": null,
#        "gender": null,
#        "profile_image_url": null,
#        "is_verified": true
#      },
#      "clinic": {
#        "id": 1,
#        "name": "Health Plus Medical Center",
#        "website_url": null,
#        "profile_image_url": null,
#        "description": "Leading medical center",
#        "established_year": 2010,
#        "total_staff": 50
#      },
#      "license_number": "MD123456",
#      "consultation_fee": "50.00",
#      "online_consultation_fee": "30.00",
#      "average_consultation_time": 30,
#      "is_online_consultation_available": true,
#      "rating": "4.80",
#      "total_reviews": 150,
#      "total_patients": 500,
#      "bio": "Experienced cardiologist with 10+ years of practice",
#      "years_of_experience": 10,
#      "specialty": {
#        "id": 1,
#        "name": "Cardiology",
#        "description": "Heart and cardiovascular system",
#        "category": "specialist"
#      },
#      "is_primary": false,
#      "is_active": true,
#      "verified_by": null,
#      "created_at": "2024-01-15T10:30:00Z",
#      "updated_at": "2024-01-15T10:30:00Z"
#    }
#    ```

# 6. **Error Response Examples:**

#    **Doctor Not Found (404):**
#    ```json
#    {
#      "error": "Doctor not found"
#    }
#    ```

#    **Invalid Query Parameters (400):**
#    ```json
#    {
#      "error": "Error retrieving doctors: invalid literal for int() with base 10: 'invalid'"
#    }
#    ```

# 7. **Test Coverage:**
#    - ✅ Public access (no authentication required)
#    - ✅ Pagination functionality
#    - ✅ Filtering by specialty, clinic, online consultation, primary care
#    - ✅ Multiple filter combinations
#    - ✅ Ordering by rating and name
#    - ✅ Exclusion of inactive doctors
#    - ✅ Empty result handling
#    - ✅ Non-existent doctor handling
#    - ✅ Edge cases and error conditions
# """ 