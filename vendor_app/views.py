from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Vendor
from .serializers import VendorSerializer,VendorCreateSerializer
from .utils import calculate_average_response_time, calculate_fulfillment_rate, calculate_on_time_delivery_rate,calculate_quality_rating_avg

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VendorCreateSerializer
        return VendorSerializer
    # permission_classes = [permissions.IsAuthenticated] # if auth token needed
    

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    # permission_classes = [permissions.IsAuthenticated] # if auth token needed


@api_view(['GET'])
def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
        print(vendor)
    except Vendor.DoesNotExist:
        return Response({'detail': 'Vendor not found.'}, status=status.HTTP_404_NOT_FOUND)

    performance_data = {
        'on_time_delivery_rate': calculate_on_time_delivery_rate(vendor),
        'quality_rating_avg': calculate_quality_rating_avg(vendor),
        'average_response_time': calculate_average_response_time(vendor),
        'fulfillment_rate': calculate_fulfillment_rate(vendor),
    }

    return Response(performance_data)