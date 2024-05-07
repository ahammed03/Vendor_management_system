from django.dispatch import receiver
from django.db.models.signals import post_save
from .utils import update_fulfillment_rate,update_quality_rating_avg,update_average_response_time
from .models import PurchaseOrder
# Signal handler
@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, created, **kwargs):
    print("In SIgnal")
    if not created:
        vendor = instance.vendor
        if instance.status == "completed":
            update_fulfillment_rate(vendor,PurchaseOrder=sender)
            update_quality_rating_avg(vendor,PurchaseOrder = sender)
        update_average_response_time(vendor,PurchaseOrder=sender)