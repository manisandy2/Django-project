from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, RoleViewSet, AccountMemberViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'account-members', AccountMemberViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]