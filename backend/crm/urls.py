from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # HTML-интерфейс
    path('', views.OrderListView.as_view(), name='order_list'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    
    # API endpoints (если используется DRF вместе с HTML)
    path('api/orders/', views.OrderListAPI.as_view(), name='api_order_list'),
    path('api/orders/<int:pk>/', views.OrderDetailAPI.as_view(), name='api_order_detail'),
    
    # Отчеты
    path('reports/orders/', views.OrderReportView.as_view(), name='order_report'),
    
    # Управление пользователями
    path('users/', views.UserListView.as_view(), name='user_list'),
]