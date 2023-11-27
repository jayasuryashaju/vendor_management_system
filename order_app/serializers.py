from rest_framework import serializers
from .models import PurchaseOrder

class PurchaseOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'order_date', 'items', 'quantity', 'status', 'delivery_date', 'issue_date', 'quality_rating']

    def validate(self, data):
        required_fields = ['po_number', 'vendor', 'order_date', 'items', 'quantity', 'status', 'delivery_date', 'issue_date', 'quality_rating']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError({field: f'The field {field} is required.'})

        if data['quantity'] <= 0:
            raise serializers.ValidationError({'quantity': 'Quantity must be greater than zero.'})


        return data



class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
