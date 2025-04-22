from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DestinationViewSet, LogViewSet
from .views import *

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet)
router.register(r'logs', LogViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('incoming_data', incoming_data),
]