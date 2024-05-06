from django.dispatch import receiver
from django.db.models.signals import post_save
from .utils import update_fulfillment_rate,update_quality_rating_avg
from .models import PurchaseOrder
# Signal handler
@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, created, **kwargs):
    print("")
    print("In SIgnal")
    if not created:
        vendor = instance.vendor
        print(vendor)
        print(instance.status)
        if instance.status == 'completed':
            update_fulfillment_rate(vendor,PurchaseOrder=sender)
            print("Compledt")
            if instance.delivery_date:
                print(instance.delivery_date)
                update_quality_rating_avg(vendor, instance.quality_rating,PurchaseOrder = sender)