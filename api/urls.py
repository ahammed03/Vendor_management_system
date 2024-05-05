from django.urls import path 
from .import views 
from .views import VendorListCreate

urlpatterns = [
    path('', views.index, name="index"),
    path('vendors/', VendorListCreate.as_view(), name='vendor-list-create'),

]
