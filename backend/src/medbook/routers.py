from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'doctors/documents', views.DoctorDocumentUploadView, basename='doctor_docs')
router.register(r'doctors/certificates', views.DoctorCertificateViewSet, basename='certificates')
router.register(r'doctors/languages', views.DoctorLanguageViewSet, basename='languages')
router.register(r'doctors/services', views.DoctorServiceViewSet, basename='services')
router.register(r'doctors/experience', views.DoctorExperienceViewSet, basename='experience')
router.register(r'doctors/images', views.DoctorImageUploadView, basename='doctor_images')
router.register(r'doctors/social-media', views.DoctorSocialMediaViewSet, basename='docotr_social_media')
router.register(r"doctors/working-hours", views.DoctorWorkingHourViewSet, basename="doctor_working_hours")
router.register(r"doctors/by-id", views.DoctorByIdView, basename="doctor_by_id")
router.register(r"doctors", views.DoctorsView, basename="doctor_list")

router.register(r'clinics/documents', views.ClinicDocumentUploadView, basename='clinic_docs')
router.register(r'clinics/images', views.ClinicImageUploadView, basename='clinic_images')
router.register(r'clinics/social-media', views.ClinicSocialMediaViewSet, basename='clinic_social_media')
router.register(r"clinics/working-hours", views.ClinicWorkingHourViewSet, basename="clinic_working_hours")


router.register(r'patients/images', views.PatientImageUploadView, basename='patient_images')





