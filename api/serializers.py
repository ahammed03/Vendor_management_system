from rest_framework import serializers 
from .models import Vendor,PurchaseOrder

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor 
        fields = ['id','name', 'contact_details','address']
