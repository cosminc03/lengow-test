from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from orders.models import Order
from orders.serializers import OrderSerializer


class OrderList(APIView):
    """
    List all orders
    """

    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)

        return JsonResponse(serializer.data, safe=False)


class OrderDetail(APIView):
    """
    Retrieve an order instance.
    """

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)

        return JsonResponse(serializer.data, safe=False)
