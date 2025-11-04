from rest_framework import serializers
from .models import IDEPlugin, IDEConnection, IDEEvent

class IDEPluginSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = IDEPlugin
        fields = ['id', 'user', 'user_name', 'ide_name', 'plugin_version', 'installed_at', 'last_connected', 'is_active']
        read_only_fields = ['id', 'installed_at', 'last_connected']

class IDEConnectionSerializer(serializers.ModelSerializer):
    plugin_info = serializers.CharField(source='plugin.__str__', read_only=True)
    
    class Meta:
        model = IDEConnection
        fields = ['id', 'plugin', 'plugin_info', 'connection_token', 'connected_at', 'disconnected_at', 'is_connected']
        read_only_fields = ['id', 'connected_at', 'disconnected_at']

class IDEEventSerializer(serializers.ModelSerializer):
    plugin_info = serializers.CharField(source='plugin.__str__', read_only=True)
    
    class Meta:
        model = IDEEvent
        fields = ['id', 'plugin', 'plugin_info', 'event_type', 'file_path', 'line_number', 'timestamp', 'details']
        read_only_fields = ['id', 'timestamp']