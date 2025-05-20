from rest_framework.views import APIView
from rest_framework.response import Response
from apps.orders.models import Order

class OrderAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()[:20]
        data = [{
            'id': o.id,
            'client': o.client_name,
            'status': o.get_status_display()
        } for o in orders]
        return Response(data)