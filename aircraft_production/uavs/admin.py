from django.contrib import admin
from .models import Uavs

@admin.register(Uavs)
class UavsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'model', 'status', 'stock_quantity', 'created_at', 'updated_at')
    search_fields = ('name', 'model', 'serial_number')
    list_filter = ('status',)
    ordering = ('-created_at',)
    list_per_page = 10
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('General Info', {'fields': ('id', 'name', 'model', 'description', 'serial_number')}),
        ('Status & Stock', {'fields': ('status', 'stock_quantity')}),
        ('Important Dates', {'fields': ('created_at', 'updated_at')}),
    )
