from rest_framework import serializers
from .models import Destination, Log




class DestinationSerializer(serializers.ModelSerializer):
    # created_by_username = serializers.ReadOnlyField(source='created_by.username')
    # updated_by_username = serializers.ReadOnlyField(source='updated_by.username')
    # account_name = serializers.ReadOnlyField(source='account.name')

    class Meta:
        model = Destination
        fields = [
            'account', 'url', 'headers',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['created_at', 'updated_at']

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
