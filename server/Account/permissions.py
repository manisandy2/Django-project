from rest_framework.permissions import BasePermission
from Profile.models import AccountMember

class IsAdminForAccount(BasePermission):
    """
    Allows access only to admin members of the account.
    """
    def has_permission(self, request, view):
        account_id = view.kwargs.get('account_id') or request.data.get('account_id')
        if not account_id:
            return False
        try:
            member = AccountMember.objects.get(account_id=account_id, user=request.user)
            return member.role.role_name.lower() == "admin"
        except AccountMember.DoesNotExist:
            return False

class IsMemberOfAccount(BasePermission):
    """
    Allows read-only access to any account member.
    """
    def has_permission(self, request, view):
        account_id = view.kwargs.get('account_id') or request.query_params.get('account_id')
        if not account_id:
            return False
        return AccountMember.objects.filter(account_id=account_id, user=request.user).exists()