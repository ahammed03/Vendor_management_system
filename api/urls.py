from django.urls import path 
from .import views 
from .views import VendorListCreate,VendorRetrieveUpdateDestroy,PurchaseOrderListView,PurchaseOrderRetrieveUpdateDestroy

urlpatterns = [
    path('', views.index, name="index"),
    path('vendors/', VendorListCreate.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDestroy.as_view(), name='vendor-retrieve-update-destroy'),
    path('purchase_orders/',PurchaseOrderListView.as_view(),name='purchase-order-list-create' ),
    path('purchase_orders/<int:pk>/',PurchaseOrderRetrieveUpdateDestroy.as_view(),name='purchase-order-retrieve-update-destroy' )

]
