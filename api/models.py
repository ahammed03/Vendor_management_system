from django.db import models

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
        ('canceled', 'Canceled')
    ]
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True)
    original_delivery_date = models.DateTimeField(null=True)
    items = models.JSONField()
    quantity = models.IntegerField() 
    status = models.CharField(max_length=100,choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.id)

class HistoricPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(null = True)
    quality_rating_avg = models.FloatField(null = True)
    average_response_time =  models.FloatField(null = True)
    fulfillment_rate =  models.FloatField(null = True)

    def __str__(self) -> str:
        return self.vendor.name