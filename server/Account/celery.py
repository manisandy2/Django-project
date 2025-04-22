# from __future__ import absolute_import
# import requests
# import os
# from celery import Celery
# from celery import shared_task
# from .models import Destination, Log
# from datetime import datetime

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

# app = Celery('server')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()




# @shared_task
# def send_data_to_destinations(account_id, data):
#     """
#     Asynchronously send data to all destinations associated with the account.
#     """
#     # Retrieve the destinations for the account
#     destinations = Destination.objects.filter(account_id=account_id)

#     if not destinations:
#         return "No destinations found for the account."

#     # For each destination, send the data
#     for destination in destinations:
#         # Prepare the headers (you can customize this as needed)
#         headers = {
#             "Content-Type": "application/json",
#             "Accept": "*/*",
#             **destination.headers,  # Assuming the headers are stored in the Destination model
#         }

#         # Send the data to the destination
#         try:
#             response = requests.request(
#                 method=destination.http_method,  # GET, POST, etc.
#                 url=destination.url,
#                 json=data,  # Send data as JSON
#                 headers=headers
#             )

#             # Check if the request was successful
#             status = "success" if response.status_code == 200 else "failed"

#             # Log the event (Log model is where we store logs)
#             Log.objects.create(
#                 account_id=account_id,
#                 received_timestamp=datetime.now(),
#                 processed_timestamp=datetime.now(),
#                 destination_id=destination.id,
#                 received_data=data,
#                 status=status
#             )

#             # You could also check the response content to decide success/failure more precisely
#             if status == "failed":
#                 # You can log detailed error or retry logic here
#                 pass

#         except requests.exceptions.RequestException as e:
#             # Log the error in case of failure to send the data
#             Log.objects.create(
#                 account_id=account_id,
#                 received_timestamp=datetime.now(),
#                 processed_timestamp=datetime.now(),
#                 destination_id=destination.id,
#                 received_data=data,
#                 status="failed"
#             )
#             # Optionally send an alert or retry the request
#             print(f"Failed to send data to destination {destination.url}: {e}")
            
#     return "Data sent to all destinations successfully."