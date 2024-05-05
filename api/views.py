from django.shortcuts import render,HttpResponse
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer
from rest_framework import generics
from uuid import uuid4
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