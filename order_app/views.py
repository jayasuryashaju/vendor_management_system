from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction


from .models import PurchaseOrder,HistoricalPerformance
from .serializers import PurchaseOrderSerializer, PurchaseOrderCreateSerializer
from vendor_app.utils import calculate_average_response_time, calculate_fulfillment_rate, calculate_on_time_delivery_rate,calculate_quality_rating_avg



class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = PurchaseOrderCreateSerializer

    def get_queryset(self):

        vendor_id = self.request.query_params.get('vendor_id', None)
        if vendor_id:
            queryset = PurchaseOrder.objects.filter(vendor__id=vendor_id)
        else:
            queryset = PurchaseOrder.objects.all()

        return queryset

    def perform_create(self, serializer):
        serializer.save()

class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


@api_view(['POST', 'GET'])
def acknowledge_purchase_order(request, po_id):
    try:
        with transaction.atomic():
            po = PurchaseOrder.objects.get(pk=po_id)
            po.acknowledgment_date = timezone.now()
            po.save()

            vendor = po.vendor

            # Recalculate average_response_time
            vendor.average_response_time = calculate_average_response_time(vendor)
            vendor.save()

            # Update historical performance
            HistoricalPerformance.objects.create(
                vendor=vendor,
                date = timezone.now(),
                on_time_delivery_rate=calculate_on_time_delivery_rate(vendor),
                quality_rating_avg=calculate_quality_rating_avg(vendor),
                average_response_time=calculate_average_response_time(vendor),
                fulfillment_rate=calculate_fulfillment_rate(vendor),
            )

            serializer = PurchaseOrderSerializer(po)
            return Response(serializer.data)
    except PurchaseOrder.DoesNotExist:
        return Response({'detail': 'Purchase order not found.'}, status=status.HTTP_404_NOT_FOUND)