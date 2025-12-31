from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PassengerTripViewSet, 
    CustomerRequestViewSet, 
    DealViewSet, 
    UserProfileViewSet
)

router = DefaultRouter()
router.register(r'trips', PassengerTripViewSet)
router.register(r'requests', CustomerRequestViewSet)
router.register(r'deals', DealViewSet)
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('api/', include(router.urls)),
]