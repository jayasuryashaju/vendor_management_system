from django.urls import path
from .views import (
    PurchaseOrderListCreateView,
    PurchaseOrderDetailView,
    acknowledge_purchase_order
)

urlpatterns = [

    path('', PurchaseOrderListCreateView.as_view(), name='purchase_order_list_create'),
    path('<int:pk>/', PurchaseOrderDetailView.as_view(), name='purchase_order_detail'),

    path('<int:po_id>/acknowledge/', acknowledge_purchase_order, name='acknowledge_purchase_order'),


]
