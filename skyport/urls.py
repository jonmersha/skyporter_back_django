from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TripViewSet, 
    TravelerProductViewSet, 
    CustomerRequestViewSet, 
    DealViewSet, 
    EnquiryViewSet
)

# Initialize the router
router = DefaultRouter()

# Marketplace Endpoints
router.register(r'trips', TripViewSet, basename='trip')
router.register(r'traveler-products', TravelerProductViewSet, basename='travelerproduct')
router.register(r'customer-requests', CustomerRequestViewSet, basename='customerrequest')

# Transaction & Communication Endpoints
# Basenames are explicitly set to handle the custom get_queryset logic
router.register(r'deals', DealViewSet, basename='deal')
router.register(r'enquiries', EnquiryViewSet, basename='enquiry')

urlpatterns = [
    # API Routes
    path('', include(router.urls)),
]