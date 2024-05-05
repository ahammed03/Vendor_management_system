from rest_framework import serializers 
from .models import Vendor,PurchaseOrder

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor 
        fields = ['id','name', 'contact_details','address']
class PurchaseOrderListSerializer(serializers.ModelSerializer):
    class Meta :
        model = PurchaseOrder
        fields = '__all__'
class PurchaseOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder 
        fields = ['vendor', 'items', 'quantity']

