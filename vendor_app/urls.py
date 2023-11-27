from django.urls import path
from .views import (
    VendorListCreateView,
    VendorDetailView,
    vendor_performance
)

urlpatterns = [

    path('', VendorListCreateView.as_view(), name='vendor_list_create'),
    path('<int:pk>/', VendorDetailView.as_view(), name='vendor_detail'),
    path('<int:vendor_id>/performance/', vendor_performance, name='vendor_performance'),


]
