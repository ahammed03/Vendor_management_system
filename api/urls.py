from django.urls import path 
from .import views 
from .views import VendorListCreate
from .views import VendorRetrieveUpdateDestroy
from .views import PurchaseOrderListView 
from .views import PurchaseOrderRetrieveUpdateDestroy
from .views import VendorPerformanceListView 
from .views import PurchaseOrderAcknowledgeUpdateView

urlpatterns = [
    path('', views.index, name="index"),
    path('vendors/', VendorListCreate.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDestroy.as_view(), name='vendor-retrieve-update-destroy'),
    path('purchase_orders/',PurchaseOrderListView.as_view(),name='purchase-order-list-create' ),
    path('purchase_orders/<int:pk>/',PurchaseOrderRetrieveUpdateDestroy.as_view(),name='purchase-order-retrieve-update-destroy' ),
    path('vendor/<int:pk>/performance/',VendorPerformanceListView.as_view(),name='vendor-performance-list' ),
    path('purchase_orders/<int:pk>/acknowledgement_date/',PurchaseOrderAcknowledgeUpdateView.as_view(),name='purchase-order-acknowledge' ),
]
