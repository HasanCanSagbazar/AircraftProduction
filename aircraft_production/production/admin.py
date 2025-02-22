from django.contrib import admin
from .models import PartProduction

@admin.register(PartProduction)
class PartProductionAdmin(admin.ModelAdmin):
    list_display = ('id', 'part', 'team', 'status', 'serial_number', 'is_used', 'added_by', 'created_at', 'updated_at')
    list_filter = ('status', 'team', 'is_used')
    search_fields = ('part__name', 'team__name', 'added_by__username', 'serial_number')
    ordering = ('-created_at',)
    list_editable = ('status', 'is_used')
    list_per_page = 20
    readonly_fields = ('id', 'created_at', 'updated_at', 'serial_number')
    fieldsets = (
        ('Part Production Info', {'fields': ('id', 'part', 'team', 'status', 'serial_number', 'is_used', 'added_by')}),
        ('Important Dates', {'fields': ('created_at', 'updated_at')}),
    )
