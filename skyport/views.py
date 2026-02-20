from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Trip, TravelerProduct, CustomerRequest, Deal, Enquiry, DealStatus
from .serializers import (
    TripSerializer, TravelerProductSerializer, 
    CustomerRequestSerializer, DealSerializer, EnquirySerializer
)

class TripViewSet(viewsets.ModelViewSet):
    """
    Handles Travelers posting their journeys.
    """
    queryset = Trip.objects.filter(is_active=True).order_by('-arrival_date')
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(traveler=self.request.user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """GET /api/trips/me/ - Trips posted by current traveler"""
        my_trips = Trip.objects.filter(traveler=request.user).order_by('-arrival_date')
        serializer = self.get_serializer(my_trips, many=True)
        return Response(serializer.data)


class TravelerProductViewSet(viewsets.ModelViewSet):
    """
    Handles Travelers listing specific items they have for sale/transport.
    """
    queryset = TravelerProduct.objects.all().order_by('-created_at')
    serializer_class = TravelerProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(traveler=self.request.user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """GET /api/traveler-products/me/"""
        my_products = TravelerProduct.objects.filter(traveler=request.user)
        serializer = self.get_serializer(my_products, many=True)
        return Response(serializer.data)


class CustomerRequestViewSet(viewsets.ModelViewSet):
    """
    Handles Customers posting items they need transported.
    """
    queryset = CustomerRequest.objects.filter(is_open=True).order_by('-preferred_delivery_date')
    serializer_class = CustomerRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """GET /api/customer-requests/me/"""
        my_requests = CustomerRequest.objects.filter(customer=request.user)
        serializer = self.get_serializer(my_requests, many=True)
        return Response(serializer.data)


class EnquiryViewSet(viewsets.ModelViewSet):
    """
    Handles the messaging/contact phase before a Deal is formed.
    """
    serializer_class = EnquirySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users see their own sent or received messages
        return Enquiry.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        ).select_related('sender', 'receiver', 'trip', 'product', 'request')

    def perform_create(self, serializer):
        """
        Auto-detect the receiver from the linked item if not provided.
        """
        trip = serializer.validated_data.get('trip')
        product = serializer.validated_data.get('product')
        req = serializer.validated_data.get('request')
        receiver = serializer.validated_data.get('receiver')

        if not receiver:
            if trip: receiver = trip.traveler
            elif product: receiver = product.traveler
            elif req: receiver = req.customer

        serializer.save(sender=self.request.user, receiver=receiver)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """
        POST /api/enquiries/{id}/accept/
        The Bridge: Converts an Enquiry into a formal Deal.
        """
        enquiry = self.get_object()
        
        if enquiry.receiver != request.user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        if enquiry.is_accepted:
            return Response({"error": "Already accepted"}, status=status.HTTP_400_BAD_REQUEST)

        # ROLE LOGIC: Define who is Traveler and who is Customer
        if enquiry.trip or enquiry.product:
            traveler, customer = enquiry.receiver, enquiry.sender
        else: 
            traveler, customer = enquiry.sender, enquiry.receiver

        # Initial Price Logic
        price = 0
        if enquiry.product: price = enquiry.product.price + enquiry.product.expected_reward
        elif enquiry.request: price = enquiry.request.budget
        elif enquiry.trip: price = enquiry.trip.other_fee  # Starting point

        # Create Deal
        deal = Deal.objects.create(
            customer=customer,
            traveler=traveler,
            trip=enquiry.trip,
            product=enquiry.product,
            request=enquiry.request,
            final_price=price,
            status=DealStatus.PENDING
        )

        enquiry.is_accepted = True
        enquiry.save()

        return Response({
            "deal_id": deal.id,
            "status": "ACCEPTED",
            "message": f"Deal created with {traveler.username if request.user == customer else customer.username}"
        }, status=status.HTTP_201_CREATED)



class DealViewSet(viewsets.ModelViewSet):
    """
    Handles the lifecycle of a transaction from Pending to Completed.
    """
    serializer_class = DealSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Deal.objects.filter(
            Q(customer=self.request.user) | Q(traveler=self.request.user)
        ).select_related('customer', 'traveler', 'trip', 'product', 'request')

    @action(detail=False, methods=['get'])
    def me(self, request):
        my_deals = self.get_queryset().order_by('-updated_at')
        serializer = self.get_serializer(my_deals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        PATCH /api/deals/{id}/update_status/
        Advances the shipment status.
        """
        deal = self.get_object()
        new_status = request.data.get('status')

        if new_status not in DealStatus.values:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        # Traveler controls logistics
        if new_status in [DealStatus.PURCHASED, DealStatus.IN_TRANSIT, DealStatus.ARRIVED]:
            if request.user != deal.traveler:
                return Response({"error": "Only travelers update logistics"}, status=status.HTTP_403_FORBIDDEN)

        # Customer controls final closure
        if new_status == DealStatus.COMPLETED:
            if request.user != deal.customer:
                return Response({"error": "Only customer confirms receipt"}, status=status.HTTP_403_FORBIDDEN)

        deal.status = new_status
        deal.save()
        return Response({"status": deal.status, "message": "Deal status updated"})