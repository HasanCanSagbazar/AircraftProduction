from django.contrib import admin
from .models import OTP

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('employee', 'code', 'is_used', 'expires_at', 'created_at')
    list_filter = ('is_used', 'expires_at')
    search_fields = ('employee__email', 'code')
    readonly_fields = ('created_at', 'expires_at', 'code')
    fieldsets = (
        (None, {
            'fields': ('employee', 'code', 'is_used', 'expires_at', 'created_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.is_used:
            obj.mark_used()
        super().save_model(request, obj, form, change)