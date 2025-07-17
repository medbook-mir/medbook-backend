from django.contrib import admin

from .models import Clinic, Doctor, Patient, Specialty, User


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
