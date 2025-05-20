from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet, 
    UserViewSet,
    LocationViewSet,
    ManagerStatusViewSet,
    BlacklistViewSet,
    OrderBlacklistView
)

router = DefaultRouter()
router.register(r'blacklist', BlacklistViewSet, basename='blacklist')

# Регистрация ViewSets
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'users', UserViewSet, basename='user')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'manager-statuses', ManagerStatusViewSet, basename='manager-status')
router.register(r'blacklist', BlacklistViewSet, basename='blacklist')

# Дополнительные endpoints
urlpatterns = [
    path('', include(router.urls)),
    
    path(
        'orders/<int:pk>/blacklist/',
        OrderBlacklistView.as_view({'post': 'blacklist'}),
        name='order-blacklist'
    ),

    # Документация API
    path('docs/', include_docs_urls(
        title='CRM API',
        description='API для системы управления заявками',
        public=False
    )),
    
    # Авторизация
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
] + router.urls