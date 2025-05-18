from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CityViewSet,
    ClientViewSet,
    ManagerViewSet,
    RequestViewSet,
    telegram_webhook
)

router = DefaultRouter()
router.register(r'cities', CityViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'managers', ManagerViewSet)
router.register(r'requests', RequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('telegram-webhook/', telegram_webhook, name='telegram-webhook'),
]