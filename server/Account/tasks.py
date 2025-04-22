# import requests
# from celery import shared_task
# from django.utils import timezone
# from .models import Log, Account, Destination
# from datetime import datetime
# import json

# @shared_task
# def send_to_destination_task(event_id, account_id, data, received_timestamp_str):

#     received_time = datetime.fromisoformat(received_timestamp_str)
#     account = Account.objects.get(id=account_id)
#     destinations = Destination.objects.filter(account=account)

#     for destination in destinations:
#         try:
#             headers = destination.headers or {}
#             response = requests.request(
#                 method=destination.method,
#                 url=destination.url,
#                 json=data,
#                 headers=headers
#             )
#             status = 'success' if 200 <= response.status_code < 300 else 'failed'
#         except Exception as e:
#             status = 'failed'

#         Log.objects.create(
#             event_id=event_id,
#             account=account,
#             destination=destination,
#             received_timestamp=received_time,
#             processed_timestamp=timezone.now(),
#             received_data=data,
#             status=status
#         )