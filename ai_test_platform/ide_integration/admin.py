from django.contrib import admin
from .models import IDEPlugin, IDEConnection, IDEEvent

@admin.register(IDEPlugin)
class IDEPluginAdmin(admin.ModelAdmin):
    list_display = ['user', 'ide_name', 'plugin_version', 'installed_at', 'is_active']
    list_filter = ['ide_name', 'installed_at', 'is_active', 'user']
    search_fields = ['user__username', 'ide_name']
    readonly_fields = ['installed_at', 'last_connected']

@admin.register(IDEConnection)
class IDEConnectionAdmin(admin.ModelAdmin):
    list_display = ['plugin', 'connection_token', 'connected_at', 'is_connected']
    list_filter = ['connected_at', 'is_connected', 'plugin__ide_name']
    search_fields = ['plugin__user__username', 'connection_token']
    readonly_fields = ['connected_at', 'disconnected_at']

@admin.register(IDEEvent)
class IDEEventAdmin(admin.ModelAdmin):
    list_display = ['plugin', 'event_type', 'file_path', 'timestamp']
    list_filter = ['event_type', 'timestamp', 'plugin__ide_name']
    search_fields = ['plugin__user__username', 'file_path']
    readonly_fields = ['timestamp']