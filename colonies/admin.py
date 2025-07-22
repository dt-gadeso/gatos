from django.contrib import admin
from .models import Zone, Municipality, Location


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    ordering = ('name',)



@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'address', 'municipality', 'latitude', 'longitude', 'created_at')
    list_filter = ('municipality', 'created_at')
    search_fields = ('nombre', 'address', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

