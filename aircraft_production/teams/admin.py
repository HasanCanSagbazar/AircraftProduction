from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_assemble', 'is_producer', 'created_at', 'updated_at')
    list_filter = ('is_assemble', 'is_producer')
    search_fields = ('name',)
    ordering = ('created_at',)
    readonly_fields = ('id','is_assemble', 'is_producer', 'created_at', 'updated_at')
