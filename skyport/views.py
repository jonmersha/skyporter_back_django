from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import *
from .serializers import *

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.filter(is_active=True)
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(traveler=self.request.user)

class TravelerProductViewSet(viewsets.ModelViewSet):
    queryset = TravelerProduct.objects.all().order_by('-created_at')
    serializer_class = TravelerProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(traveler=self.request.user)

class CustomerRequestViewSet(viewsets.ModelViewSet):
    queryset = CustomerRequest.objects.filter(is_open=True)
    serializer_class = CustomerRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class DealViewSet(viewsets.ModelViewSet):
    serializer_class = DealSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users only see deals they are involved in
        return Deal.objects.filter(Q(customer=self.request.user) | Q(traveler=self.request.user))

class EnquiryViewSet(viewsets.ModelViewSet):
    serializer_class = EnquirySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users see enquiries they sent or received
        return Enquiry.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        enquiry = self.get_object()
        if enquiry.receiver != request.user:
            return Response({"error": "Only the receiver can accept"}, status=403)
        
        enquiry.is_accepted = True
        enquiry.save()

        # Logic to create the formal Deal based on who initiated
        is_request = enquiry.request is not None
        Deal.objects.create(
            customer=enquiry.receiver if is_request else enquiry.sender,
            traveler=enquiry.sender if is_request else enquiry.receiver,
            trip=enquiry.trip,
            product=enquiry.product,
            request=enquiry.request,
            final_price=0, # To be updated during negotiation
            status=DealStatus.NEGOTIATING
        )
        return Response({"status": "Accepted, Deal created"})