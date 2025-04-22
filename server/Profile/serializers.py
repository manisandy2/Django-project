from rest_framework import serializers
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('app_secret_token', 'created_at', 'updated_at')




class AccountMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountMember
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')





############################################################################################################

