from django.db.models import Count, Avg, F
from django.utils import timezone

def calculate_on_time_delivery_rate(vendor):
    completed_pos = vendor.purchaseorder_set.filter(status='completed')
    on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
    total_completed_pos = completed_pos.count()

    on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100 if total_completed_pos != 0 else 0

    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.save()

    return on_time_delivery_rate

def calculate_quality_rating_avg(vendor):
    completed_pos = vendor.purchaseorder_set.filter(status='completed').exclude(quality_rating__isnull=True)
    quality_rating_avg = completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

    vendor.quality_rating_avg = quality_rating_avg
    vendor.save()

    return quality_rating_avg

def calculate_average_response_time(vendor):
    completed_pos = vendor.purchaseorder_set.filter(status='completed').exclude(acknowledgment_date__isnull=True)
    response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_pos]
    average_response_time = sum(response_times) / len(completed_pos) if len(completed_pos) != 0 else 0

    vendor.average_response_time = average_response_time
    vendor.save()

    return average_response_time

def calculate_fulfillment_rate(vendor):
    completed_pos = vendor.purchaseorder_set.filter(status='completed')
    successful_fulfillments = completed_pos.filter(issue_date__lte=F('acknowledgment_date')).count()
    total_pos = completed_pos.count()

    fulfillment_rate = (successful_fulfillments / total_pos) * 100 if total_pos != 0 else 0

    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()

    return fulfillment_rate
