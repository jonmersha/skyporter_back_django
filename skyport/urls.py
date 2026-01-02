from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'trips', TripViewSet)
router.register(r'traveler-products', TravelerProductViewSet)
router.register(r'customer-requests', CustomerRequestViewSet)
router.register(r'deals', DealViewSet, basename='deal')
router.register(r'enquiries', EnquiryViewSet, basename='enquiry')

urlpatterns = [
    path('', include(router.urls)),
]