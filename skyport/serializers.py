from rest_framework import serializers
from .models import Trip, TravelerProduct, CustomerRequest, Enquiry, Deal, ProductImage

class TripSerializer(serializers.ModelSerializer):
    traveler_name = serializers.ReadOnlyField(source='traveler.username')
    traveler_phone = serializers.ReadOnlyField(source='traveler.phone_number')
    traveler_email = serializers.ReadOnlyField(source='traveler.email')

    class Meta:
        model = Trip
        fields = [
            'id', 'traveler', 'traveler_name', 'traveler_phone', 'traveler_email',
            'departure_city', 'destination_city', 'departure_date', 'arrival_date',
            'laptop_fee', 'mobile_fee', 'cosmetic_fee', 'other_fee', 'is_active'
        ]
        # This prevents the "This field is required" error in Flutter
        read_only_fields = ['traveler']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class TravelerProductSerializer(serializers.ModelSerializer):
    traveler_name = serializers.ReadOnlyField(source='traveler.username')
    traveler_phone = serializers.ReadOnlyField(source='traveler.phone_number')
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = TravelerProduct
        fields = [
            'id', 'traveler', 'traveler_name', 'traveler_phone', 'name', 
            'description', 'category', 'price', 'expected_reward', 
            'arrival_date', 'expiration_time', 'images', 'created_at'
        ]

class CustomerRequestSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.username')
    customer_phone = serializers.ReadOnlyField(source='customer.phone_number')
    customer_email = serializers.ReadOnlyField(source='customer.email')

    class Meta:
        model = CustomerRequest
        fields = [
            'id', 'customer', 'customer_name', 'customer_phone', 'customer_email',
            'title', 'request_type', 'category', 'from_city', 'to_city', 
            'preferred_delivery_date', 'budget', 'description', 'is_open'
        ]
        # ADD THIS LINE:
        read_only_fields = ['customer']
        
class EnquirySerializer(serializers.ModelSerializer):
    sender_name = serializers.ReadOnlyField(source='sender.username')
    receiver_name = serializers.ReadOnlyField(source='receiver.username')
    # Sender needs receiver's phone to launch WhatsApp
    receiver_phone = serializers.ReadOnlyField(source='receiver.phone_number')
    enquiry_type = serializers.ReadOnlyField() # Calls the @property in your model

    class Meta:
        model = Enquiry
        fields = [
            'id', 'sender', 'sender_name', 'receiver', 'receiver_name', 
            'receiver_phone', 'trip', 'product', 'request', 
            'message', 'is_accepted', 'enquiry_type', 'created_at'
        ]

class DealSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.username')
    traveler_name = serializers.ReadOnlyField(source='traveler.username')
    # Accessing contact points for both parties in the deal
    customer_phone = serializers.ReadOnlyField(source='customer.phone_number')
    traveler_phone = serializers.ReadOnlyField(source='traveler.phone_number')
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Deal
        fields = [
            'id', 'customer', 'customer_name', 'customer_phone',
            'traveler', 'traveler_name', 'traveler_phone',
            'trip', 'product', 'request', 'status', 'status_display', 
            'final_price', 'updated_at'
        ]