from django.contrib import admin
from .models import UavsAssembly, AssemblyPart


@admin.register(UavsAssembly)
class UavsAssemblyAdmin(admin.ModelAdmin):
    list_display = ('id', 'aircraft_model', 'team', 'assembly_status', 'added_by', 'created_at', 'updated_at')
    search_fields = ('aircraft_model__name', 'team__name', 'added_by__name')
    list_filter = ('assembly_status', 'team')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(AssemblyPart)
class AssemblyPartAdmin(admin.ModelAdmin):
    list_display = ('id', 'assembly', 'part', 'installed_at')
    search_fields = ('assembly__aircraft_model__name', 'part__name')
    list_filter = ('assembly__assembly_status', 'part__name')
    ordering = ('-installed_at',)
    readonly_fields = ('id', 'installed_at')


