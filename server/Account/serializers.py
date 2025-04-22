from .models import *
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'created_at', 'updated_at',
            'created_by', 'updated_by',
            'is_active', 'is_staff'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']