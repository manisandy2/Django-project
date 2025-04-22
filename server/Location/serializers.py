from rest_framework import serializers
from .models import Destination, Log


class DestinationSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    updated_by_username = serializers.ReadOnlyField(source='updated_by.username')
    account_name = serializers.ReadOnlyField(source='account.name')

    class Meta:
        model = Destination
        fields = [
            'id',
            'account', 'account_name',
            'url', 'method', 'headers',
            'created_at', 'updated_at',
            'created_by', 'created_by_username',
            'updated_by', 'updated_by_username',
        ]
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')


class LogSerializer(serializers.ModelSerializer):
    account_name = serializers.ReadOnlyField(source='account.name')
    destination_url = serializers.ReadOnlyField(source='destination.url')

    class Meta:
        model = Log
        fields = [
            'event_id',
            'account', 'account_name',
            'destination', 'destination_url',
            'received_timestamp', 'processed_timestamp',
            'received_data', 'status',
            'received_data', 'status', 'response_message'
        ]
        read_only_fields = fields  # make log read-only through API