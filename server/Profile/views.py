from rest_framework import viewsets
from .models import Account, Role, AccountMember
from .serializers import AccountSerializer, RoleSerializer, AccountMemberSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class AccountMemberViewSet(viewsets.ModelViewSet):
    queryset = AccountMember.objects.all()
    serializer_class = AccountMemberSerializer