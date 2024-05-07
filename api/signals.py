from django.dispatch import receiver
from django.db.models.signals import post_save
from .utils import update_fulfillment_rate,update_quality_rating_avg,update_average_response_time,update_on_time_delivery_rate
from .models import PurchaseOrder,HistoricPerformance,Vendor
# Signal handler
@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, created, **kwargs):
    print("In SIgnal")
    if not created:
        vendor = instance.vendor
        print()
        if instance.original_delivery_date:
            update_on_time_delivery_rate(vendor,PurchaseOrder=sender)
        if instance.status == "completed":
            update_fulfillment_rate(vendor,PurchaseOrder=sender)
            update_quality_rating_avg(vendor,PurchaseOrder = sender)
        update_average_response_time(vendor,PurchaseOrder=sender)

@receiver(post_save,sender=Vendor)
def insert_into_historic_model(sender,instance,created,**kwargs):
    performance_metrics = Vendor.objects.get(pk = instance.pk)
    HistoricPerformance.objects.create(vendor = performance_metrics, 
                                average_response_time = performance_metrics.average_response_time, 
                                on_time_delivery_rate = performance_metrics.on_time_delivery_rate, 
                                quality_rating_avg = performance_metrics.quality_rating_avg,
                                fulfillment_rate = performance_metrics.fulfillment_rate)

