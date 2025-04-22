from django.contrib import admin
from .models import Account
from .models import AccountMember
from .models import Role


# @admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     list_display = ('name', 'website', 'created_at', 'updated_at')
#     search_fields = ('account_name',)


# @admin.register(AccountMember)
# class AccountMemberAdmin(admin.ModelAdmin):
#     list_display = ('account', 'user', 'role', 'created_at')
#     search_fields = ('user__email', 'account__account_name')


# @admin.register(Role)
# class RoleAdmin(admin.ModelAdmin):
#     list_display = ('role_name', 'created_at', 'updated_at')

# from django.contrib import admin
# from .models import Account, Role, AccountMember

# Register the Account model
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'secret_token', 'website', 'created_at', 'updated_at', 'created_by', 'updated_by')
    search_fields = ('name', 'website')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('id', 'secret_token', 'created_at', 'updated_at')

# Register the Role model
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_name', 'created_at', 'updated_at')
    search_fields = ('role_name',)
    list_filter = ('created_at', 'updated_at')

# Register the AccountMember model
@admin.register(AccountMember)
class AccountMemberAdmin(admin.ModelAdmin):
    list_display = ('account', 'user', 'role', 'created_at', 'updated_at')
    search_fields = ('user__email', 'account__name', 'role__role_name')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')