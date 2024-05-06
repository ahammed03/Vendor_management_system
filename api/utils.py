
from django.db import models


# Helper functions to update performance metrics
def update_on_time_delivery_rate(vendor,PurchaseOrder):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_orders = completed_orders.filter(delivery_date=models.F('acknowledgment_date'))
    total_completed = completed_orders.count()
    total_on_time = on_time_orders.count()
    if total_completed > 0:
        vendor.on_time_delivery_rate = (total_on_time / total_completed) * 100
        vendor.save()

def update_quality_rating_avg(vendor, quality_rating, PurchaseOrder):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    total_completed = completed_orders.count()
    total_quality_rating = completed_orders.aggregate(models.Avg('quality_rating'))['quality_rating__avg']
    if total_completed > 0:
        vendor.quality_rating_avg = total_quality_rating
        vendor.save()

def update_average_response_time(vendor, response_time,PurchaseOrder):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status = 'completed' or 'canceled', acknowledgment_date__isnull=False)
    total_completed = completed_orders.count()
    total_response_time = completed_orders.aggregate(models.Avg(response_time))['{}__avg'.format(response_time)]
    if total_completed > 0:
        vendor.average_response_time = total_response_time
        vendor.save()

def update_fulfillment_rate(vendor,PurchaseOrder):
    print("Ful fill ment")
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    successful_orders = completed_orders.exclude(quality_rating = 0)
    total_completed = completed_orders.count()
    total_successful = successful_orders.count()
    if total_completed > 0 and total_successful > 0:
        vendor.fulfillment_rate = (total_successful / total_completed) * 100
        vendor.save()