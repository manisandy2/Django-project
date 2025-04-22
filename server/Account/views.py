# import asyncio
# import httpx
# from django.utils import timezone
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status as drf_status
# from .models import Account, Log, Destination
# from rest_framework.permissions import *
# from rest_framework import generics
# from .models import CustomUser, Role, AccountMember
# from .serializers import *
# from rest_framework.response import Response
# from .tasks import send_to_destination_task
# import json
# from rest_framework import viewsets
# from django.core.exceptions import ValidationError
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# from .models import Account
# from permissions import *
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Account
# from .serializers import AccountSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Log
# from .serializers import LogSerializer
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Account
# from .serializers import AccountSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from django.http import JsonResponse
# from django_ratelimit.exceptions import RatelimitException
# from django.http import JsonResponse
# from django_ratelimit.decorators import ratelimit
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Account, Log
# from .serializers import LogSerializer
# from django.core.cache import cache
# import datetime

# class DataHandlerView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Validate headers
#         app_secret = request.headers.get('CL-X-TOKEN')
#         event_id = request.headers.get('CL-X-EVENT-ID')

#         if not app_secret or not event_id:
#             return Response({'error': 'Missing CL-X-TOKEN or CL-X-EVENT-ID in headers'}, status=drf_status.HTTP_400_BAD_REQUEST)

#         # Identify account
#         try:
#             account = Account.objects.get(app_secret_token=app_secret)
#         except Account.DoesNotExist:
#             return Response({'error': 'Invalid app secret token'}, status=drf_status.HTTP_403_FORBIDDEN)

#         received_data = request.data
#         received_time = timezone.now()

#         # Launch async task
#         asyncio.create_task(self.process_and_forward(account, event_id, received_data, received_time))

#         return Response({'message': 'Data received and being processed'}, status=drf_status.HTTP_202_ACCEPTED)

#     async def process_and_forward(self, account, event_id, data, received_time):
#         destinations = account.destinations.all()
#         tasks = []

#         for destination in destinations:
#             tasks.append(self.send_to_destination(destination, account, event_id, data, received_time))

#         await asyncio.gather(*tasks)

#     async def send_to_destination(self, destination, account, event_id, data, received_time):
#         async with httpx.AsyncClient() as client:
#             try:
#                 headers = destination.headers or {}
#                 response = await client.request(
#                     method=destination.method,
#                     url=destination.url,
#                     json=data,
#                     headers=headers
#                 )
#                 status = 'success' if response.status_code in range(200, 300) else 'failed'
#             except Exception:
#                 status = 'failed'

#         # Log result
#         Log.objects.create(
#             event_id=event_id,
#             account=account,
#             destination=destination,
#             received_timestamp=received_time,
#             processed_timestamp=timezone.now(),
#             received_data=data,
#             status=status
#         )


# class RegisterUserView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = RegisterUserSerializer
#     permission_classes = [IsAuthenticated]  # Ensure only authenticated admins can register others

#     def perform_create(self, serializer):
#         user = serializer.save()
#         role = Role.objects.get(role_name="Normal User")  # default
#         account_id = self.request.data.get('account_id')
#         is_admin = self.request.data.get('is_admin', False)

#         if is_admin:
#             role = Role.objects.get(role_name="Admin")

#         AccountMember.objects.create(
#             account_id=account_id,
#             user=user,
#             role=role,
#             created_by=self.request.user,
#             updated_by=self.request.user
#         )

# class AccountMemberViewSet(viewsets.ModelViewSet):
#     queryset = AccountMember.objects.all()
#     serializer_class = AccountMemberSerializer

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'destroy']:
#             return [IsAdminUserOfAccount()]
#         return [IsNormalOrAdminOfAccount()]
    



# class DataHandlerView(APIView):
#     def post(self, request, *args, **kwargs):
#         app_secret = request.headers.get('CL-X-TOKEN')
#         event_id = request.headers.get('CL-X-EVENT-ID')

#         if not app_secret or not event_id:
#             return Response({'error': 'Missing required headers'}, status=400)

#         try:
#             account = Account.objects.get(app_secret_token=app_secret)
#         except Account.DoesNotExist:
#             return Response({'error': 'Invalid app secret token'}, status=403)

#         received_data = request.data
#         received_time = timezone.now()

#         send_to_destination_task.delay(
#             event_id,
#             str(account.id),
#             received_data,
#             received_time.isoformat()
#         )

#         return Response({'message': 'Data received and processing started'}, status=202)
    




# class AccountCreateView(APIView):
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         try:
#             # Validate email and website fields
#             email = data.get('email')
#             website = data.get('website')

#             # Email validation
#             if email:
#                 validate_email(email)
            
#             # Website validation
#             if website:
#                 validate_website(website)
            
#             # Create Account if valid
#             account = Account.objects.create(
#                 account_name=data['account_name'],
#                 app_secret_token=data['app_secret_token'],
#                 website=website,
#                 email=email,
#                 created_by=request.user,
#                 updated_by=request.user
#             )
#             return Response({"message": "Data Received"}, status=status.HTTP_201_CREATED)

#         except ValidationError as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
        

# from django.db.models import Q
# from .models import Account

# def search_accounts(account_name=None, email=None):
#     query = Q()
#     if account_name:
#         query &= Q(account_name__icontains=account_name)
#     if email:
#         query &= Q(email__icontains=email)

#     accounts = Account.objects.filter(query)
#     return accounts

# def search_destinations(account_id=None, url=None, method=None):
#     query = Q(account__id=account_id) if account_id else Q()

#     if url:
#         query &= Q(url__icontains=url)
#     if method:
#         query &= Q(method=method)

#     destinations = Destination.objects.filter(query)
#     return destinations


# from .models import Log

# def search_logs(account_id=None, status=None):
#     query = Q()
#     if account_id:
#         query &= Q(account__id=account_id)
#     if status:
#         query &= Q(status=status)

#     logs = Log.objects.filter(query)
#     return logs




# class AccountSearchView(APIView):
#     def get(self, request, *args, **kwargs):
#         account_name = request.query_params.get('account_name', None)
#         email = request.query_params.get('email', None)
        
#         accounts = search_accounts(account_name=account_name, email=email)
        
#         serializer = AccountSerializer(accounts, many=True)
#         return Response(serializer.data)
    



# class LogSearchView(APIView):
#     def get(self, request, *args, **kwargs):
#         account_id = request.query_params.get('account_id', None)
#         status = request.query_params.get('status', None)
        
#         logs = search_logs(account_id=account_id, status=status)
        
#         serializer = LogSerializer(logs, many=True)
#         return Response(serializer.data)
    

# class AccountDestinationSearchView(APIView):
#     def get(self, request, *args, **kwargs):
#         account_name = request.query_params.get('account_name', None)
#         url = request.query_params.get('url', None)

#         # Search accounts and prefetch related destinations
#         accounts = Account.objects.prefetch_related('destination_set')

#         if account_name:
#             accounts = accounts.filter(account_name__icontains=account_name)

#         destinations = Destination.objects.filter(url__icontains=url) if url else None

#         # Now fetch only related destinations from the filtered accounts
#         accounts = accounts.filter(destination__in=destinations) if destinations else accounts

#         accounts = accounts.all()  # Execute the final query

#         serializer = AccountSerializer(accounts, many=True)
#         return Response(serializer.data)
    



# class AccountListView(APIView):
#     @method_decorator(cache_page(60*15))  # Cache the view for 15 minutes
#     def get(self, request, *args, **kwargs):
#         accounts = Account.objects.all()
#         serializer = AccountSerializer(accounts, many=True)
#         return Response(serializer.data)
    

# from django.core.cache import cache
# from .models import Account

# def get_filtered_accounts(account_name=None):
#     cache_key = f"accounts_{account_name}"
#     accounts = cache.get(cache_key)

#     if not accounts:
#         accounts = Account.objects.filter(account_name__icontains=account_name)
#         cache.set(cache_key, accounts, timeout=60*15)  # Cache for 15 minutes

#     return accounts



# class DataHandlerView(APIView):

#     @ratelimit(key='header:CL-X-TOKEN', rate='5/second', burst=5)
#     def post(self, request, *args, **kwargs):
#         app_secret_token = request.META.get('HTTP_CL_X_TOKEN')
        
#         if not app_secret_token:
#             return JsonResponse({"detail": "App secret token missing"}, status=400)

#         # Verify the account associated with the token
#         try:
#             account = Account.objects.get(app_secret_token=app_secret_token)
#         except Account.DoesNotExist:
#             return JsonResponse({"detail": "Invalid app secret token"}, status=400)

#         # Handle the data processing and sending to destinations
#         event_id = request.META.get('HTTP_CL_X_EVENT_ID')
#         if not event_id:
#             return JsonResponse({"detail": "Event ID missing"}, status=400)

#         # Process the incoming data and send it asynchronously
#         data = request.data  # Data received in the body

#         # Log the data processing event
#         log_entry = Log.objects.create(
#             account=account,
#             received_timestamp=datetime.now(),
#             destination_id=1,  # Example destination ID, replace with actual logic
#             received_data=data,
#             status="Processing"
#         )

#         # Simulate data sending to destinations
#         send_data_to_destinations(account, data)

#         # After processing, log the processed timestamp and status
#         log_entry.processed_timestamp = datetime.now()
#         log_entry.status = "Success"
#         log_entry.save()

#         return JsonResponse({"detail": "Data received"}, status=200)
    



# class DataHandlerView(APIView):
#     @ratelimit(key='header:CL-X-TOKEN', rate='5/second', burst=5)
#     def post(self, request, *args, **kwargs):
#         # Handle rate limit exceeded
#         if getattr(request, 'limited', False):
#             return JsonResponse({"detail": "Rate limit exceeded. Try again later."}, status=429)
        
#         # Regular data handling code...




# class DataHandlerView(APIView):
#     @swagger_auto_schema(
#         operation_description="Receive data and send it to various destinations",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'event': openapi.Schema(type=openapi.TYPE_STRING, description="Event name"),
#                 'data': openapi.Schema(type=openapi.TYPE_OBJECT, description="Event data"),
#             },
#         ),
#         responses={
#             200: openapi.Response(
#                 description="Data successfully received",
#                 examples={
#                     "application/json": {
#                         "detail": "Data received"
#                     }
#                 }
#             ),
#             400: openapi.Response(
#                 description="Invalid data or missing token",
#                 examples={
#                     "application/json": {
#                         "detail": "Invalid app secret token"
#                     }
#                 }
#             ),
#             429: openapi.Response(
#                 description="Rate limit exceeded",
#                 examples={
#                     "application/json": {
#                         "detail": "Rate limit exceeded. Try again later."
#                     }
#                 }
#             ),
#         }
#     )
#     def post(self, request):
#         # Your view logic
#         return Response({"detail": "Data received"}, status=status.HTTP_200_OK)
    
# class AccountUpdateView(APIView):
#     def put(self, request, *args, **kwargs):
#         account_id = kwargs['pk']
#         account = Account.objects.get(id=account_id)
#         serializer = AccountSerializer(account, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()

#             # Invalidate cache after update
#             cache.delete(f"accounts_{account.account_name}")  # Cache invalidation

#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)



############################################################################################
from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]