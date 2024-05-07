
from django.db import models
from datetime import datetime



def update_on_time_delivery_rate(vendor, PurchaseOrder):
    completed_orders = PurchaseOrder.objects.filter(status='completed',vendor=vendor)
    on_time_deliveries = completed_orders.filter(original_delivery_date__lte=models.F('delivery_date'))
    on_time_delivery_rate = (on_time_deliveries.count() / completed_orders.count()) * 100 if completed_orders.count() else 0
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.save()

def update_quality_rating_avg(vendor, PurchaseOrder):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    total_completed = completed_orders.count()
    total_quality_rating = completed_orders.aggregate(models.Avg('quality_rating'))['quality_rating__avg']
    if total_completed > 0:
        vendor.quality_rating_avg = total_quality_rating
        vendor.save()

def update_average_response_time(vendor,PurchaseOrder):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status = 'completed' or 'canceled', acknowledgment_date__isnull=False)
    total_completed = completed_orders.count()
    if total_completed > 0:
        time_differences = []
        for order in completed_orders:
            time_difference = dates_difference(order.acknowledgment_date,order.issue_date)
            time_differences.append(time_difference) 
        diff = sum(time_differences) / total_completed
        vendor.average_response_time = diff
        vendor.save()


def update_fulfillment_rate(vendor,PurchaseOrder):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    successful_orders = completed_orders.exclude(quality_rating = 0)
    total_completed = completed_orders.count()
    total_successful = successful_orders.count()
    if total_completed > 0 and total_successful > 0:
        vendor.fulfillment_rate = (total_successful / total_completed) * 100
        vendor.save()




def dates_difference(end,start):
    end_str = end.strftime('%Y-%m-%d %H:%M:%S')  # Remove microseconds
    start_str = start.strftime('%Y-%m-%d %H:%M:%S')  # Remove microseconds
    end_datetime = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
    start_datetime = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
    time_diff = end_datetime - start_datetime
    return time_diff.total_seconds()