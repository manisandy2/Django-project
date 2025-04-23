from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Destination, Log
from .serializers import DestinationSerializer, LogSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from django.utils.timezone import now
from Profile.models import Account
from .models import Destination, Log
from .tasks import send_data_to_destination
from rest_framework.exceptions import PermissionDenied
import uuid
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from ratelimit.decorators import *
from ratelimit import rate_limited
from django_ratelimit.decorators import ratelimit
from Location.tasks import send_data_to_destination
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=True, methods=['post'])
    
    def test_destination(self, request, pk=None):
        destination = self.get_object()
        try:
            test_payload = {"sample": "test"}
            headers = destination.headers

            if destination.method == "GET":
                response = requests.get(destination.url, params=test_payload, headers=headers)
            else:
                response = requests.request(destination.method, destination.url, json=test_payload, headers=headers)

            return Response({
                "status": response.status_code,
                "response": response.text
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class LogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Log.objects.none()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        account_ids = user.accounts.values_list('id', flat=True)
        
        queryset = Log.objects.filter(account__id__in=account_ids)

        account = self.request.query_params.get('account')
        if account:
            queryset = queryset.filter(account_id=account)

        return queryset
    
    def perform_create(self, serializer):
        user = self.request.user
        account = serializer.validated_data['account']
        if account.id not in user.accounts.values_list('id', flat=True):
            raise PermissionDenied("You don't have access to this account")
        serializer.save()

class LogListView(ListAPIView):
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['destination_id', 'status', 'received_timestamp', 'processed_timestamp']
    ordering_fields = ['received_timestamp', 'processed_timestamp']

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if not account_id:
            return Log.objects.none()
        return Log.objects.filter(account_id=account_id)
    

class AccountRateThrottle(UserRateThrottle):
    rate = '5/second'

@api_view(['POST'])
@throttle_classes([AccountRateThrottle])
class IncomingDataView(APIView):
    @method_decorator(ratelimit(key='user_or_ip', rate='5/s', method='POST', block=True))
    def post(self, request, *args, **kwargs):
        event_id = request.headers.get("CL-X-EVENT-ID")
        token = request.headers.get("CL-X-TOKEN")
        data = request.data

        if not token:
            return Response({"success": False, "message": "Unauthenticated"}, status=401)
        if not isinstance(data, dict) or not event_id:
            return Response({"success": False, "message": "Invalid Data"}, status=400)

        try:
            account = Account.objects.get(app_secret_token=token)
        except Account.DoesNotExist:
            return Response({"success": False, "message": "Unauthenticated"}, status=401)

        destinations = Destination.objects.filter(account=account)
        for dest in destinations:
            send_data_to_destination.delay(
                event_id=event_id,
                account_id=account.id,
                destination_id=dest.id,
                destination_url=dest.url,
                method=dest.http_method,
                headers=dest.headers,
                payload=data
            )

        return Response({"success": True, "message": "Data Received"}, status=200)

