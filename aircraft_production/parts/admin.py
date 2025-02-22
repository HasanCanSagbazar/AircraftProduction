from django.contrib import admin
from .models import Part

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'aircraft', 'team', 'serial_number', 'stock_quantity', 'is_active', 'created_at')
    list_filter = ('category', 'aircraft', 'team', 'is_active')
    ordering = ('-created_at',)
    search_fields = ('name', 'serial_number', 'aircraft__name', 'team__name')
    fieldsets = (
        ('General Information', {
            'fields': ('id', 'name', 'category', 'description', 'serial_number') 
        }),
        ('Stock Information', {
            'fields': ('aircraft', 'team', 'stock_quantity', 'is_active')
        }),
    )
    readonly_fields = ('id',)  
    list_editable = ('stock_quantity', 'is_active')
    list_per_page = 20
