from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique= True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    def __str__(self) -> str:
        return self.name

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('acknowledge', 'Acknowledge' ),
        ('canceled', 'Canceled')
    ]
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True)
    items = models.JSONField()
    quantity = models.IntegerField() 
    status = models.CharField(max_length=100,choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.id)

# Signals
@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, created, **kwargs):
    if not created:
        print("hello")
        vendor = instance.vendor
        update_fulfillment_rate(vendor)
        if instance.status == 'completed':
            print("dbjf")
            # update_on_time_delivery_rate(vendor)
        #     update_quality_rating_avg(vendor, instance.quality_rating)
        # if instance.acknowledgment_date:
        #     update_average_response_time(vendor, instance.acknowledgment_date - instance.issue_date)
        

# Helper functions to update performance metrics
def update_on_time_delivery_rate(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_orders = completed_orders.filter(delivery_date__lte=models.F('acknowledgment_date'))
    total_completed = completed_orders.count()
    total_on_time = on_time_orders.count()
    if total_completed > 0:
        vendor.on_time_delivery_rate = (total_on_time / total_completed) * 100
        vendor.save()

def update_quality_rating_avg(vendor, quality_rating):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    total_completed = completed_orders.count()
    total_quality_rating = completed_orders.aggregate(models.Avg('quality_rating'))['quality_rating__avg']
    if total_completed > 0:
        vendor.quality_rating_avg = total_quality_rating
        vendor.save()

def update_average_response_time(vendor, response_time):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status = 'completed' or 'canceled', acknowledgment_date__isnull=False)
    total_completed = completed_orders.count()
    total_response_time = completed_orders.aggregate(models.Avg(response_time))['{}__avg'.format(response_time)]
    if total_completed > 0:
        vendor.average_response_time = total_response_time
        vendor.save()

def update_fulfillment_rate(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    successful_orders = completed_orders.exclude(quality_rating = 0)
    total_completed = completed_orders.count()
    total_successful = successful_orders.count()
    if total_completed > 0 and total_successful > 0:
        vendor.fulfillment_rate = (total_successful / total_completed) * 100
        vendor.save()