from django.urls import path 
from .import views 
from .views import VendorListCreate,VendorRetrieveUpdateDestroy

urlpatterns = [
    path('', views.index, name="index"),
    path('vendors/', VendorListCreate.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDestroy.as_view(), name='vendor-retrieve-update-destroy'),

]
