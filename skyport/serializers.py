from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, RequestType, DealStatus, Trip, 
    TravelerProduct, ProductImage, CustomerRequest, 
    Deal, Enquiry
)

# 1. Image Serializer (Nested in TravelerProduct)
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

# 2. Trip Serializer (The Service Menu)
class TripSerializer(serializers.ModelSerializer):
    traveler_name = serializers.ReadOnlyField(source='traveler.username')

    class Meta:
        model = Trip
        fields = [
            'id', 'traveler', 'traveler_name', 'departure_city', 
            'destination_city', 'arrival_date', 'laptop_fee', 
            'mobile_fee', 'cosmetic_fee', 'other_fee_base', 'is_active'
        ]
        read_only_fields = ['traveler']

# # 3. Traveler Product Serializer (Personal Shopping)
# class TravelerProductSerializer(serializers.ModelSerializer):
#     images = ProductImageSerializer(many=True, read_only=True)
#     traveler_name = serializers.ReadOnlyField(source='traveler.username')
    
#     # Total price calculated for the UI
#     total_price = serializers.SerializerMethodField()

#     class Meta:
#         model = TravelerProduct
#         fields = [
#             'id', 'traveler', 'traveler_name', 'name', 'description', 
#             'category', 'price', 'expected_reward', 'total_price',
#             'arrival_date', 'expiration_time', 'created_at', 'images'
#         ]
#         read_only_fields = ['traveler']

#     def get_total_price(self, obj):
#         return obj.price + obj.expected_reward
# serializers.py

class TravelerProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    traveler_name = serializers.ReadOnlyField(source='traveler.username')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = TravelerProduct
        fields = '__all__'
        read_only_fields = ['traveler']

    def get_total_price(self, obj):
        return obj.price + obj.expected_reward

    def create(self, validated_data):
        # 1. Get the list of images from the request
        # 'uploaded_images' must match the key used in Flutter
        request = self.context.get('request')
        images_data = request.FILES.getlist('uploaded_images')

        # 2. Create the product first
        product = TravelerProduct.objects.create(**validated_data)

        # 3. Create the ProductImage objects linked to this product
        for image in images_data:
            ProductImage.objects.create(product=product, image=image)

        return product
# 4. Customer Request Serializer (Marketplace Posts)
class CustomerRequestSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        model = CustomerRequest
        fields = [
            'id', 'customer', 'customer_name', 'title', 'request_type', 
            'category', 'from_city', 'to_city', 'preferred_delivery_date', 
            'budget', 'description', 'is_open'
        ]
        read_only_fields = ['customer']

# 5. Enquiry Serializer (The Communication Phase)
class EnquirySerializer(serializers.ModelSerializer):
    sender_name = serializers.ReadOnlyField(source='sender.username')
    receiver_name = serializers.ReadOnlyField(source='receiver.username')
    enquiry_type = serializers.ReadOnlyField() # Calls the @property in the model

    class Meta:
        model = Enquiry
        fields = [
            'id', 'sender', 'sender_name', 'receiver', 'receiver_name', 
            'trip', 'product', 'request', 'message', 'is_accepted', 
            'enquiry_type', 'created_at'
        ]
        read_only_fields = ['sender', 'is_accepted']

# 6. Deal Serializer (The Final Transaction)
class DealSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.username')
    traveler_name = serializers.ReadOnlyField(source='traveler.username')
    
    # Status display name for the UI
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Deal
        fields = [
            'id', 'customer', 'customer_name', 'traveler', 'traveler_name', 
            'trip', 'product', 'request', 'status', 'status_display', 
            'final_price', 'updated_at'
        ]
        read_only_fields = ['customer', 'traveler', 'updated_at']