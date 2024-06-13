from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # You can customize the fields displayed and actions available here
    list_display = (
        "username",
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "is_staff",
        "date_joined",
        "last_login",
    )  # Adjust fields as needed
    search_fields = (
        "username",
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "address_line1",
        "city",
        "state",
        "postal_code",
    )  # Adjust fields as needed
