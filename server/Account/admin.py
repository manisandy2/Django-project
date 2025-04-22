from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import CustomUser
from django.utils.translation import gettext_lazy as _

# @admin.register(CustomUser)
# class UserAdmin(BaseUserAdmin):
#     ordering = ['email']
#     list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
#     list_filter = ['is_staff', 'is_superuser', 'is_active']
#     search_fields = ['email', 'first_name', 'last_name']

#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
#         (_('Permissions'), {
#             'fields': (
#                 'is_active', 'is_staff', 'is_superuser',
#                 'groups', 'user_permissions'
#             )
#         }),
#         (_('Important dates'), {'fields': ('last_login',)}),
#         (_('Tracking'), {'fields': ('created_by', 'updated_by', 'created_at', 'updated_at')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2'),
#         }),
#     )

#     readonly_fields = ['created_at', 'updated_at']