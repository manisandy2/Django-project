from rest_framework.permissions import BasePermission
# from .models import AccountMember

# class IsAdminUserOfAccount(BasePermission):
#     def has_permission(self, request, view):
        
#         return AccountMember.objects.filter(
#             user=request.user,
#             account_id=request.data.get('account_id'),
#             role__role_name="Admin"
#         ).exists()

# class IsNormalOrAdminOfAccount(BasePermission):
#     def has_permission(self, request, view):
#         return AccountMember.objects.filter(
#             user=request.user,
#             account_id=request.data.get('account_id')
#         ).exists()
    

# class IsAdminUserOfAccount(BasePermission):
#     def has_permission(self, request, view):
        
#         account_id = view.kwargs.get('account_id')  
#         if not account_id:
#             return False
        
        
#         try:
#             account_member = AccountMember.objects.get(account_id=account_id, user=request.user)
#             return account_member.role.role_name == 'Admin'
#         except AccountMember.DoesNotExist:
#             return False


# class IsNormalOrAdminOfAccount(BasePermission):
    
#     def has_permission(self, request, view):
        
#         account_id = view.kwargs.get('account_id')  
#         if not account_id:
#             return False
        
        
#         try:
#             account_member = AccountMember.objects.get(account_id=account_id, user=request.user)
#             if request.method in ['GET', 'PUT', 'PATCH']: 
#                 return True
#             if request.method in ['POST', 'DELETE']:  
#                 return account_member.role.role_name == 'Admin'
#             return False
#         except AccountMember.DoesNotExist:
#             return False