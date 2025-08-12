# import io
# import re
# import sys

# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password
# from django.test import TestCase, override_settings
# from rest_framework import status
# from rest_framework.test import APIClient
# from rest_framework_simplejwt.tokens import RefreshToken

# from medbook.models import Clinic, Doctor

# User = get_user_model()


# @override_settings(EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend")
# class SignupAndVerifyTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.test_user = User.objects.create(
#             username="authuser",
#             email="authuser@example.com",
#             phone_number="1234567890",
#             password=make_password("authpassword123"),
#             is_active=True,
#             role="SUPERADMIN",
#         )
#         refresh = RefreshToken.for_user(self.test_user)
#         self.token = str(refresh.access_token)
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
#         self._stdout = sys.stdout
#         self.output = io.StringIO()
#         sys.stdout = self.output

#     def tearDown(self):
#         sys.stdout = self._stdout

#     def test_signup_success(self):
#         payload = {
#             "username": "testuser@example.com",
#             "first_name": "Test",
#             "last_name": "User",
#             "password": "testpassword123",
#             "repeat_password": "testpassword123",
#             "birthday": "26-02-1990",
#         }
#         response = self.client.post("/api/auth/send/", payload, format="json")

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(
#             response.data,
#             {
#                 "message": "Verification code sent to email. Check your email for the code."
#             },
#         )

#         user = User.objects.get(username="testuser@example.com")
#         self.assertFalse(user.is_active)
#         self.assertIsNotNone(user.email_code)

#         email_output = self.output.getvalue()
#         self.assertIn("Your email verification code is:", email_output)
#         code_match = re.search(
#             r"Your email verification code is:\s*(\d{4})", email_output, re.IGNORECASE
#         )
#         self.assertIsNotNone(code_match)
#         stored_code = user.email_code
#         self.assertEqual(code_match.group(1), stored_code)

#     def test_verify_code_success(self):
#         user = User.objects.create(
#             username="verifyuser",
#             first_name="Verify",
#             last_name="User",
#             email="verifyuser@example.com",
#             phone_number="1234567890",
#             password=make_password("verifyPassword123"),
#             date_joined="2025-05-10T12:00:00Z",
#             is_active=False,
#             email_code="1234",
#         )

#         payload = {"email_code": "1234"}
#         response = self.client.post("/api/auth/verify/", payload, format="json")

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(
#             response.data, {"message": "Verification successful. You can now log in."}
#         )

#         user.refresh_from_db()
#         self.assertTrue(user.is_active)
#         self.assertIsNone(user.email_code)

#     def test_verify_code_failure(self):
#         user = User.objects.create(
#             username="verifyfail",
#             first_name="VerifyFail",
#             last_name="User",
#             email="verifyfail@example.com",
#             phone_number="1234567890",
#             password=make_password("verifyFail123"),
#             date_joined="2025-05-10T12:00:00Z",
#             is_active=False,
#             email_code="1234",
#         )

#         payload = {"email_code": "6543"}
#         response = self.client.post("/api/auth/verify/", payload, format="json")

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data, {"error": "Invalid verification code."})

#         user.refresh_from_db()
#         self.assertFalse(user.is_active)
#         self.assertEqual(user.email_code, "1234")


# @override_settings(EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend")
# class DoctorClinicSignupAndVerifyTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#         self.test_user = User.objects.create(
#             username="adminuser",
#             email="admin@example.com",
#             phone_number="1234567890",
#             password=make_password("adminpass123"),
#             is_active=True,
#             role="SUPERADMIN",
#         )
#         refresh = RefreshToken.for_user(self.test_user)
#         self.token = str(refresh.access_token)
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

#         self._stdout = sys.stdout
#         self.output = io.StringIO()
#         sys.stdout = self.output

#     def tearDown(self):
#         sys.stdout = self._stdout

#     def _signup_and_verify_email_test(self, payload, expected_model, expected_role):
#         response = self.client.post("/api/doctor/signup/", payload, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         user = User.objects.get(email=payload["email"])
#         self.assertFalse(user.is_active)
#         self.assertIsNotNone(user.email_code)

#         email_output = self.output.getvalue()
#         self.assertIn("Your email verification code is:", email_output)

#         code_match = re.search(
#             r"Your email verification code is:\s*(\d{4})", email_output, re.IGNORECASE
#         )
#         self.assertIsNotNone(code_match)
#         self.assertEqual(code_match.group(1), user.email_code)

#         self.assertTrue(expected_model.objects.filter(user=user).exists())
#         self.assertEqual(user.role.lower(), expected_role.lower())

#     def test_doctor_signup_success(self):
#         payload = {
#             "role": "doctor",
#             "first_name": "John",
#             "last_name": "Doe",
#             "email": "doctor@example.com",
#             "password": "strongpassword123",
#         }
#         self._signup_and_verify_email_test(
#             payload, expected_model=Doctor, expected_role="doctor"
#         )

#     def test_clinic_signup_success(self):
#         payload = {
#             "role": "clinic",
#             "clinic_name": "Health Center",
#             "email": "clinic@example.com",
#             "password": "clinicpassword123",
#         }
#         self._signup_and_verify_email_test(
#             payload, expected_model=Clinic, expected_role="clinic"
#         )

#     def test_doctor_verification_success(self):
#         user = User.objects.create(
#             username="doctor@example.com",
#             email="doctor@example.com",
#             is_active=False,
#             email_code="1234",
#         )
#         Doctor.objects.create(user=user)

#         payload = {"email_code": "1234"}
#         response = self.client.post("/api/auth/verify/", payload, format="json")

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(
#             response.data, {"message": "Verification successful. You can now log in."}
#         )

#         user.refresh_from_db()
#         self.assertTrue(user.is_active)
#         self.assertIsNone(user.email_code)

#     def test_clinic_verification_success(self):
#         user = User.objects.create(
#             username="clinic@example.com",
#             email="clinic@example.com",
#             is_active=False,
#             email_code="5678",
#         )
#         Clinic.objects.create(user=user, name="Clinic Name")

#         payload = {"email_code": "5678"}
#         response = self.client.post("/api/auth/verify/", payload, format="json")

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(
#             response.data, {"message": "Verification successful. You can now log in."}
#         )

#         user.refresh_from_db()
#         self.assertTrue(user.is_active)
#         self.assertIsNone(user.email_code)

#     def test_verification_failure_invalid_code(self):
#         user = User.objects.create(
#             username="clinic@example.com",
#             email="clinic@example.com",
#             is_active=False,
#             email_code="9999",
#         )
#         Clinic.objects.create(user=user, name="Another Clinic")

#         payload = {"email_code": "0000"}
#         response = self.client.post("/api/auth/verify/", payload, format="json")

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data, {"error": "Invalid verification code."})

#         user.refresh_from_db()
#         self.assertFalse(user.is_active)
#         self.assertEqual(user.email_code, "9999")
