from django.db import models
# from django.contrib.auth.models import User
from Profile.models import Account
import uuid
from Account.models import CustomUser

HTTP_METHOD_CHOICES = [
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('PATCH', 'PATCH'),
    ('DELETE', 'DELETE'),
]

class Destination(models.Model):
    account = models.ForeignKey(Account, related_name='destinations', on_delete=models.CASCADE)

    url = models.URLField()  
    method = models.CharField(max_length=10, choices=HTTP_METHOD_CHOICES, default='POST')  
    headers = models.JSONField()  

    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='destinations_created')  
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='destinations_updated')  

    def __str__(self):
        return f"{self.account.name} -> {self.url}"
    



class Log(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='logs')  
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='logs')  
    received_timestamp = models.DateTimeField()  
    processed_timestamp = models.DateTimeField()  
    received_data = models.JSONField()  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)  

    def __str__(self):
        return f"Event {self.event_id} ({self.status})"
    