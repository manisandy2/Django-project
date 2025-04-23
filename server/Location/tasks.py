from celery import shared_task
from .models import Destination, Log
from Profile.models import Account
from django.utils.timezone import now
import requests
import uuid

@shared_task
def send_data_to_destination(event_id, account_id, destination_id, destination_url, method, headers, payload):
    processed_time = now()
    status_str = "failed"
    
    try:
        if method == "GET":
            response = requests.get(destination_url, headers=headers, params=payload)
        else:
            response = requests.request(method, destination_url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            status_str = "success"
    except Exception:
        pass

    Log.objects.create(
        event_id=event_id,
        account_id=account_id,
        destination_id=destination_id,
        received_data=payload,
        received_timestamp=now(),
        processed_timestamp=processed_time,
        status=status_str,
    )