from django.shortcuts import render,HttpResponse
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer,PurchaseOrderListSerializer, PurchaseOrderCreateSerializer
from rest_framework import generics
from uuid import uuid4
from datetime import timedelta
from django.utils import timezone
# Create your views here.

def index(request):
    return HttpResponse("Vendor Management System")

class VendorListCreate(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    def perform_create(self, serializer):
        serializer.save(vendor_code=uuid4()) 

class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PurchaseOrderListSerializer
        elif self.request.method == 'POST':
            return PurchaseOrderCreateSerializer
    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        vendor = self.request.query_params.get('filter')
        if vendor:
            queryset = queryset.filter(vendor=vendor)
        return queryset
    def perform_create(self, serializer):
        serializer.save(po_number=uuid4(), delivery_date = timezone.now() + timedelta(days = 7)) 

class PurchaseOrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderListSerializer
    # customize the serializer for put