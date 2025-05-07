from django.contrib import admin

from product_bot.models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone_number",
        "email",
        "created_at",
    )
    search_fields = ("first_name", "last_name", "phone_number")
