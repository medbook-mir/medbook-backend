from django.contrib import admin

from .models import User


@admin.register(User)
class TariffFunctionalityAdmin(admin.ModelAdmin):
    list_display_links = ("id", "username")
    list_display = (
        "id",
        "username",
        "email",
        "phone_number",
        "birthday",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_active",)
    search_fields = ("username",)
    list_per_page = 20
