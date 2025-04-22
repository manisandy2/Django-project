from rest_framework import serializers
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


from rest_framework import serializers
from .models import Account, Role, AccountMember
from Account.models import CustomUser  

class AccountSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    updated_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Account
        fields = ('id', 'name', 'secret_token', 'website', 'created_at', 'updated_at', 'created_by', 'updated_by')

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'role_name', 'created_at', 'updated_at')

class AccountMemberSerializer(serializers.ModelSerializer):
    account = AccountSerializer()  # Nest Account serializer
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())  # Assuming CustomUser is in Account
    role = RoleSerializer()  # Nest Role serializer
    created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    updated_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = AccountMember
        fields = ('account', 'user', 'role', 'created_at', 'updated_at', 'created_by', 'updated_by')