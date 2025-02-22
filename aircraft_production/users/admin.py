from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ("id", "first_name", "last_name", "email", "team", "role", "position", "shift", "is_active")
    list_filter = ("team", "shift", "is_active")
    search_fields = ("first_name", "last_name", "email", "phone_number")
    ordering = ("first_name", "last_name")
    readonly_fields = ("id", "created_at", "updated_at", "last_login")

    fieldsets = (
        ("Personal Info", {"fields": ("id", "first_name", "last_name", "email", "phone_number", "date_of_birth")}),
        ("Team Info", {"fields": ("team", "role", "position")}),
        ("Shift & Status", {"fields": ("shift", "is_active", "last_login")}),
        ("Important Dates", {"fields": ("created_at", "updated_at")}),
        ("Security", {"fields": ("password",)}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (
            "New Employee",
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "email", "phone_number", "password1", "password2", "team", "position", "shift", "is_active"),
            },
        ),
    )


