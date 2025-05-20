"""
API версии 1.
Содержит все endpoint'ы для работы с CRM системой.
"""
from rest_framework.routers import DefaultRouter
from .views import *

# Создаем router для автоматической генерации URL
api_v1_router = DefaultRouter()

# Регистрируем ViewSets
api_v1_router.register(r'orders', OrderViewSet, basename='order')
api_v1_router.register(r'users', UserViewSet, basename='user')
api_v1_router.register(r'locations', LocationViewSet, basename='location')
api_v1_router.register(r'blacklist', BlacklistViewSet, basename='blacklist')
api_v1_router.register(r'manager-statuses', ManagerStatusViewSet, basename='managerstatus')

# Дополнительные endpoints
api_v1_router.register(r'reports/orders', OrderReportViewSet, basename='order-report')
api_v1_router.register(r'reports/managers', ManagerReportViewSet, basename='manager-report')

urlpatterns = api_v1_router.urls