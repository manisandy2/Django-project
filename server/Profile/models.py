from django.db import models
import uuid
from django.utils.crypto import get_random_string
from Account.models import CustomUser


def generate_secret_token():
    return get_random_string(50)


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # account id
    name = models.CharField(max_length=255)  # account name (mandatory)
    secret_token = models.CharField(max_length=100, default=generate_secret_token, editable=False)  # auto-generated
    website = models.URLField(blank=True, null=True)  # optional

    # website = models.URLField(validators=[validate_website], blank=True, null=True)
    # email = models.EmailField(validators=[validate_email], blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # mandatory
    updated_at = models.DateTimeField(auto_now=True)      # mandatory
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='accounts_created')  # mandatory
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='accounts_updated')  # mandatory

    def __str__(self):
        return self.name
    
class Role(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Normal User', 'Normal User'),
    ]

    id = models.AutoField(primary_key=True)  
    role_name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return self.role_name

    
    
class AccountMember(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='account_memberships')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='account_members')

    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='account_members_created')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='account_members_updated')

    class Meta:
        unique_together = ('account', 'user')  

    def __str__(self):
        return f"{self.user.email} - {self.account.name} ({self.role.name})"
    
 