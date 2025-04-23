from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DestinationViewSet, send_data_to_destination
from .views import *

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path("server/incoming_data", IncomingDataView),
    path("logs/", LogListView.as_view(), name="log-list"),
]