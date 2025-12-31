# from rest_framework import viewsets, permissions, filters
# from .model import PassengerTrip, CustomerRequest, Deal
# from .serializers import (
#     PassengerTripSerializer, 
#     CustomerRequestSerializer, 
#     DealSerializer
# )
# from django.db.models import Q

# class PassengerTripViewSet(viewsets.ModelViewSet):
#     """Viewset for travelers to post their flight details"""
#     queryset = PassengerTrip.objects.all().order_by('-created_at')
#     serializer_class = PassengerTripSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['origin', 'destination']

#     def perform_create(self, serializer):
#         # Automatically set the traveler to the logged-in user
#         serializer.save(traveler=self.request.user)

# class CustomerRequestViewSet(viewsets.ModelViewSet):
#     """Viewset for senders to request item deliveries"""
#     queryset = CustomerRequest.objects.all().order_by('-created_at')
#     serializer_class = CustomerRequestSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['pickup_location', 'delivery_destination', 'product_name']

#     def perform_create(self, serializer):
#         # Automatically set the sender to the logged-in user
#         serializer.save(sender=self.request.user)

# class DealViewSet(viewsets.ModelViewSet):
#     """Viewset for managing active agreements between users"""
#     serializer_class = DealSerializer

#     def get_queryset(self):
#         # Only show deals where the current user is either the traveler OR the sender
#         user = self.request.user
#         return Deal.objects.filter(
#             Q(request__sender=user) | Q(trip__traveler=user)
#         ).order_by('-updated_at')

#     def perform_create(self, serializer):
#         # Logic for creating a deal from the details page
#         serializer.save()

# # class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
# #     """Viewset for viewing profile and verification status"""
# #     queryset = UserProfile.objects.all()
# #     serializer_class = UserProfileSerializer

# #     def get_object(self):
# #         # Return the profile of the logged-in user
# #         return self.request.user.userprofile