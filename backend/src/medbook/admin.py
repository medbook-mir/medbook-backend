from django.contrib import admin

from .models import (
    Clinic, 
    Address,
    ClinicDocument, 
    ClinicImage, 
    ClinicSocialMedia, 
    ClinicWorkingHour, 
    Doctor, 
    DoctorCertificate, 
    DoctorDocument, 
    DoctorEducation, 
    DoctorExperience, 
    DoctorImage, 
    DoctorLanguage, 
    DoctorService, 
    DoctorSocialMedia, 
    DoctorWorkingHour, 
    Patient, 
    PatientImage,
    Review, 
    Specialty, 
    User
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display_links = ("id", "username")
    list_display = (
        "id",
        "username",
        "role",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("username",)
    list_per_page = 25


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor",
        "clinic",
        "address_line_1",
        'address_line_2',
        "city",
        "state",
        "postal_code",
        "country",
        "is_main_address"
    )
    list_filter = ("country",)
    search_fields = ("doctor__user__username", 'clinic__user__username', 'city', 'country')
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('doctor', 'clinic')


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        'category',
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("name", 'category')
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "birthday",
        "created_at",
    )
    list_filter = ("user__is_active",)
    search_fields = ("user__first_name", "user__last_name", "user__username")
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')


@admin.register(PatientImage)
class PatientImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image",
        "instance",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("instance",)
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('instance')
    

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "is_active",
        "verified_by",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("user__email", "name", "user__username")
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')


@admin.register(ClinicImage)
class ClinicImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image",
        "instance",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("instance",)
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('instance')
    

@admin.register(ClinicDocument)
class ClinicDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "instance",
        "file",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("instance", 'name')
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('instance')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "specialty",
        "is_primary",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "is_primary", "specialty")
    search_fields = ("user__first_name", "user__last_name", "user__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')
    

@admin.register(DoctorImage)
class DoctorImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image",
        "instance",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("instance",)
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('instance')


@admin.register(DoctorDocument)
class DoctorDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "instance",
        "file",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("instance", 'name')
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('instance')


@admin.register(DoctorCertificate)
class DoctorCertificateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor",
        "verified_by",
        "title",
        "certificate_type",
        "certificate_number",
        "issue_date",
        "expiry_date",
        "verification_date",
        "is_verified",
        "is_active"
    )
    list_filter = ("is_active",)
    search_fields = ("doctor__user__username", 'title')
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('doctor')


@admin.register(DoctorLanguage)
class DoctorLanguageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor",
        "language_code",
        "language_name",
        "proficiency_level",
        
    )
    list_filter = ("language_code",)
    search_fields = ("doctor__user__username", 'language_name')
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('doctor')


@admin.register(DoctorService)
class DoctorServiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor",
        "service_name",
        "is_active",
        
    )
    list_filter = ("is_active",)
    search_fields = ("doctor__user__username", 'service_name')
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('doctor')
    

@admin.register(DoctorEducation)
class DoctorEducationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor",
        "degree",
        "field_of_study",
        "institution_name",
        "start_date",
        "end_date",
        "is_current",
    )
    list_filter = ("is_current",)
    search_fields = ("doctor__user__username", 'title')
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('doctor')


@admin.register(DoctorExperience)
class DoctorExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor",
        "position",
        "organization_name",
        "organization_type",
        "total_years",
        "start_date",
        "end_date",
        "is_current",
    )
    list_filter = ("is_current",)
    search_fields = ("doctor__user__username", 'title')
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('doctor')


@admin.register(DoctorSocialMedia)
class DoctorSocialMediaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor",
        "username",
        "profile_url",
        "platform",
    )
    list_filter = ("platform",)
    search_fields = ("doctor__user__username", 'username', 'platform')
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('doctor')


@admin.register(ClinicSocialMedia)
class ClinicSocialMediaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "clinic",
        "username",
        "profile_url",
        "platform",
    )
    list_filter = ("platform",)
    search_fields = ("clinic__user__username", 'username', 'platform')
    ordering = ("-id",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('clinic')
    

@admin.register(DoctorWorkingHour)
class DoctorWorkingHourAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor",
        "day_of_week",
        "start_time",
        "end_time",
    )
    list_filter = ("start_time", "end_time")
    search_fields = ("doctor__user__username", 'day_of_week')
    ordering = ("-id",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('doctor')
    

@admin.register(ClinicWorkingHour)
class ClinicWorkingHourAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "clinic",
        "day_of_week",
        "start_time",
        "end_time",
    )
    list_filter = ("start_time", "end_time")
    search_fields = ("clinic__user__username", 'username', 'platform')
    ordering = ("-id",)
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('clinic')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "clinic",
        "doctor",
        'title',
        "patient",
        "rating",
        "is_verified",
        "is_anonymous",
        "would_recommend",
        "helpful_count",
        "is_active",
        "created_at",
    )
    list_filter = (
        "clinic",
        "doctor",
        "patient",
        "is_verified",
        "is_anonymous",
        "would_recommend",
        "is_active",
        "created_at",
    )
    search_fields = (
        "comment",
        "clinic__name",
        "doctor__full_name",
        "patient__full_name",
    )
    readonly_fields = ("created_at", "updated_at", "helpful_count")
    ordering = ("-created_at",)
    list_display_links = ("id",)

    fieldsets = (
        (None, {
            "fields": (
                "clinic",
                "doctor",
                "patient",
                "appointment",
                "rating",
                "title",
                "comment",
            )
        }),
        ("Status & Flags", {
            "fields": (
                "is_verified",
                "is_anonymous",
                "would_recommend",
                "is_active",
            )
        }),
        ("Meta Info", {
            "fields": (
                "helpful_count",
                "created_at",
                "updated_at",
            )
        }),
    )

