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
from .tasks import push_to_destinations
from rest_framework.exceptions import PermissionDenied
import uuid

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
    

class AccountRateThrottle(UserRateThrottle):
    rate = '5/second'

@api_view(['POST'])
@throttle_classes([AccountRateThrottle])
def incoming_data(request):
    token = request.headers.get("CL-X-TOKEN")
    event_id = request.headers.get("CL-X-EVENT-ID")

    if not token or not event_id:
        return Response({"success": False, "message": "Unauthenticated"}, status=401)

    try:
        account = Account.objects.get(secret_token=token)
    except Account.DoesNotExist:
        return Response({"success": False, "message": "Unauthenticated"}, status=401)

    if not isinstance(request.data, dict):
        return Response({"success": False, "message": "Invalid Data"}, status=400)

    # Trigger async task only
    push_to_destinations.delay(event_id, account.id, request.data)

    return Response({"success": True, "message": "Data Received"})