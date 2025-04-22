from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DestinationViewSet, LogViewSet

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet)
router.register(r'logs', LogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]