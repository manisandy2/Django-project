from django.contrib import admin

from .models import Destination, Log

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'url', 'method', 'created_by', 'created_at')
    list_filter = ('method', 'account')
    search_fields = ('url', 'account__name', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'account', 'destination', 'status', 'received_timestamp', 'processed_timestamp')
    list_filter = ('status', 'account', 'destination')
    search_fields = ('event_id', 'account__name', 'destination__url')
    readonly_fields = ('event_id', 'received_data', 'received_timestamp', 'processed_timestamp')