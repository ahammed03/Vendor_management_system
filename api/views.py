from django.shortcuts import render,HttpResponse
from .models import Vendor, PurchaseOrder, HistoricPerformance
from .serializers import VendorSerializer,PurchaseOrderListSerializer, PurchaseOrderCreateSerializer, VendorPeformanceSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView 
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
        serializer.save(po_number=uuid4()) 

class PurchaseOrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderListSerializer
    # customize the serializer for put

class VendorPerformanceListView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPeformanceSerializer


class PurchaseOrderAcknowledgeUpdateView(APIView):
    def put(self,request,pk):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
            if purchase_order.status == 'completed' or purchase_order.status == 'canceled':
                return Response(f"Purchase Order Status has already Changed to {purchase_order.status}")
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "PurchaseOrder not found"}, status=404)
        try:
            po_status = request.data.get('status')
            if po_status not in ['completed', 'canceled']:
                return Response("Invalid data" , status=404) 
                # Change the status to correct    
            else:
                delivery_date = request.data.get('delivery_date')
                if po_status != "canceled":
                    if delivery_date:
                        purchase_order.delivery_date = delivery_date
                    else: 
                        purchase_order.delivery_date = timezone.now() + timedelta(days = 7)
                purchase_order.status = po_status
            purchase_order.acknowledgment_date = timezone.now() 
            purchase_order.save()
            return Response(f"Status of the order Changed to {purchase_order.status} Successfully")
        except Exception as e:
            print(e)
            return Response("Error While Creating Acknowledgement",status=500) 




def insert_into_historic_model(sender,instance,created,**kwargs):
    performance_metrics = Vendor.objects.get(pk = instance)
    HistoricPerformance.objects.create(vendor = performance_metrics, 
                                average_response_time = performance_metrics.average_response_time, 
                                on_time_delivery_rate = performance_metrics.on_time_delivery_rate, 
                                quality_rating_avg = performance_metrics.quality_rating_avg,
                                fulfillment_rate = performance_metrics.fulfillment_rate)
        

