from celery import shared_task
from .models import Destination, Log
from Profile.models import Account
from django.utils.timezone import now
import requests
import uuid

@shared_task(bind=True, autoretry_for=(requests.exceptions.RequestException,), retry_backoff=True, max_retries=3)
def push_to_destinations(self, event_id, account_id, data):
    from django.utils.timezone import now
    import requests
    import uuid
    from .models import Destination, Log
    from Profile.models import Account

    account = Account.objects.get(id=account_id)
    destinations = Destination.objects.filter(account=account)

    for dest in destinations:
        try:
            headers = dest.headers
            if dest.method == "GET":
                response = requests.get(dest.url, params=data, headers=headers)
            else:
                response = requests.request(dest.method, dest.url, json=data, headers=headers)
            status = "success" if response.status_code in [200, 201] else "failed"
            response_message = response.text
        except Exception as e:
            status = "failed"
            response_message = str(e)

        Log.objects.create(
            event_id=uuid.uuid4(),  # unique per destination
            account=account,
            destination=dest,
            received_data=data,
            received_timestamp=now(),
            processed_timestamp=now(),
            status=status,
            response_message=response_message
        )