from rest_framework import serializers
from django.contrib.auth import get_user_model

from .model import CustomerRequest, Deal, PassengerTrip

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = UserProfile # pyright: ignore[reportUndefinedVariable]
        fields = ['username', 'email', 'phone_number', 'is_verified', 'verification_level', 'bio']

class PassengerTripSerializer(serializers.ModelSerializer):
    # This lets the Flutter app show the traveler's name without a separate API call
    traveler_name = serializers.ReadOnlyField(source='traveler.username')
    is_verified = serializers.ReadOnlyField(source='traveler.userprofile.is_verified')

    class Meta:
        model = PassengerTrip
        fields = '__all__'
        read_only_fields = ['traveler']

class CustomerRequestSerializer(serializers.ModelSerializer):
    sender_name = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = CustomerRequest
        fields = '__all__'
        read_only_fields = ['sender']

class DealSerializer(serializers.ModelSerializer):
    # Nested data for the "My Deals" list in Flutter
    product_name = serializers.ReadOnlyField(source='request.product_name')
    traveler_name = serializers.ReadOnlyField(source='trip.traveler.username')
    sender_name = serializers.ReadOnlyField(source='request.sender.username')
    destination = serializers.ReadOnlyField(source='request.delivery_destination')
    
    # Status display label (e.g., "In Transit" instead of "IN_TRANSIT")
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Deal
        fields = [
            'id', 'request', 'trip', 'status', 'status_display', 
            'final_agreed_reward', 'is_paid', 'product_name', 
            'traveler_name', 'sender_name', 'destination', 'updated_at'
        ]