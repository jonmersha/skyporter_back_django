# from django.db import models
# from django.conf import settings
# from django.db import models
# from django.conf import settings
# from django.utils import timezone

# class ProductCategory(models.TextChoices):
#     ELECTRONICS = 'ELECTRONICS', 'Electronics'
#     FOOD_SUPPLEMENTS = 'FOOD_SUPPLEMENTS', 'Food Supplements'
#     MEDICINES = 'MEDICINES', 'Medicines'
#     COSMETICS = 'COSMETICS', 'Cosmetics'
#     OTHERS = 'OTHERS', 'Others'

# class TravelerProduct(models.Model):
#     traveler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offered_products')
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     category = models.CharField(max_length=30, choices=ProductCategory.choices, default=ProductCategory.OTHERS)
    
#     price = models.DecimalField(max_digits=10, decimal_places=2)  # Cost of item
#     expected_reward = models.DecimalField(max_digits=10, decimal_places=2) # Profit margin
    
#     arrival_date = models.DateField()
#     expiration_time = models.DateTimeField() # When the offer expires
#     is_active = models.BooleanField(default=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)

#     @property
#     def is_expired(self):
#         return timezone.now() > self.expiration_time

#     def __str__(self):
#         return f"{self.name} by {self.traveler.username}"

# class ProductImage(models.Model):
#     product = models.ForeignKey(TravelerProduct, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='products/')

# # Status choices for the Deal workflow
# class DealStatus(models.TextChoices):
#     PENDING = 'PENDING', 'Pending Agreement'
#     ACCEPTED = 'ACCEPTED', 'Deal Accepted'
#     PURCHASED = 'PURCHASED', 'Item Purchased'
#     IN_TRANSIT = 'IN_TRANSIT', 'In Transit'
#     ARRIVED = 'ARRIVED', 'Arrived at Destination'
#     COMPLETED = 'COMPLETED', 'Completed'
#     CANCELLED = 'CANCELLED', 'Cancelled'

# class PassengerTrip(models.Model):
#     """Model for Travelers offering luggage space"""
#     traveler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trips')
#     origin = models.CharField(max_length=100)
#     destination = models.CharField(max_length=100)
#     flight_date = models.DateField()
#     available_kg = models.DecimalField(max_digits=5, decimal_places=2)
    
#     # Pricing Policy
#     price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
#     laptop_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#     smartphone_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
#     contact_number = models.CharField(max_length=20)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.traveler.username}: {self.origin} to {self.destination}"

# class CustomerRequest(models.Model):
#     """Model for Senders requesting an item to be delivered"""
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests')
#     product_name = models.CharField(max_length=200)
#     pickup_location = models.CharField(max_length=100)
#     delivery_destination = models.CharField(max_length=100)
#     weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    
#     # Item Details
#     is_purchase_required = models.BooleanField(default=False)
#     item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#     delivery_reward = models.DecimalField(max_digits=10, decimal_places=2)
    
#     contact_number = models.CharField(max_length=20)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.product_name} to {self.delivery_destination}"

# class Deal(models.Model):
#     """Model connecting a Trip and a Request into a formal agreement"""
#     request = models.OneToOneField(CustomerRequest, on_delete=models.CASCADE, related_name='deal')
#     trip = models.ForeignKey(PassengerTrip, on_delete=models.CASCADE, related_name='deals')
    
#     # Status and Escrow
#     status = models.CharField(
#         max_length=20, 
#         choices=DealStatus.choices, 
#         default=DealStatus.PENDING
#     )
#     final_agreed_reward = models.DecimalField(max_digits=10, decimal_places=2)
#     is_paid = models.BooleanField(default=False) # True when customer pays escrow
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Deal: {self.request.product_name} ({self.status})"
from django.db import models
from django.conf import settings

# 1. Choices for Statuses and Categories
class Category(models.TextChoices):
    ELECTRONICS = "ELECTRONICS", "Electronics"
    FOOD = "FOOD_SUPPLEMENTS", "Food & Supplements"
    MEDICINE = "MEDICINES", "Medicines"
    COSMETICS = "COSMETICS", "Cosmetics"
    OTHERS = "OTHERS", "Others"

class RequestType(models.TextChoices):
    BUY_AND_TRANSPORT = "BUY_TRANSPORT", "Buy and Transport"
    TRANSPORT_ONLY = "TRANSPORT_ONLY", "Transport Only"

class DealStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    NEGOTIATING = "NEGOTIATING", "Negotiating"
    PURCHASED = "PURCHASED", "Item Purchased"
    IN_TRANSIT = "IN_TRANSIT", "In Transit"
    ARRIVED = "ARRIVED", "Arrived at Destination"
    COMPLETED = "COMPLETED", "Completed & Closed"
    CANCELLED = "CANCELLED", "Cancelled"

class Trip(models.Model):
    traveler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    departure_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    arrival_date = models.DateField()
    
    # Pricing "Menu" for this trip
    laptop_fee = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    mobile_fee = models.DecimalField(max_digits=10, decimal_places=2, default=30.00)
    cosmetic_fee = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    other_fee_base = models.DecimalField(max_digits=10, decimal_places=2, default=15.00)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.traveler.username} to {self.destination_city} ({self.arrival_date})"

class TravelerProduct(models.Model):
    traveler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listed_products")
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=Category.choices, default=Category.OTHERS)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expected_reward = models.DecimalField(max_digits=10, decimal_places=2)
    arrival_date = models.DateField()
    expiration_time = models.DateTimeField() # Life span of the post
    created_at = models.DateTimeField(auto_now_add=True)

# models.py

class ProductImage(models.Model):
    product = models.ForeignKey(
        TravelerProduct, 
        on_delete=models.CASCADE,  # <--- Add this line
        related_name='images'      # Essential for your Serializer to see the images
    )
    image = models.ImageField(upload_to='products/')

# 3. Customer Models (Requester)
class CustomerRequest(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_requests")
    title = models.CharField(max_length=200)
    request_type = models.CharField(max_length=20, choices=RequestType.choices)
    category = models.CharField(max_length=50, choices=Category.choices)
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    preferred_delivery_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2) # Price + Reward offered
    description = models.TextField()
    is_open = models.BooleanField(default=True) # Visible in Marketplace

# 4. Dealing System (The Bridge)
class Deal(models.Model):
    # Can be triggered by a Traveler Product, a Customer Request, or a Trip Inquiry
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buying_deals")
    traveler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="providing_deals")
    
    # Links to the original source
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(TravelerProduct, on_delete=models.SET_NULL, null=True, blank=True)
    request = models.ForeignKey(CustomerRequest, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(max_length=20, choices=DealStatus.choices, default=DealStatus.PENDING)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Deal {self.id}: {self.customer} & {self.traveler} ({self.status})"
class Enquiry(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_enquiries")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_enquiries")
    
    # The "Source" fields - only one will be non-null per enquiry
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(TravelerProduct, on_delete=models.CASCADE, null=True, blank=True)
    request = models.ForeignKey(CustomerRequest, on_delete=models.CASCADE, null=True, blank=True)

    message = models.TextField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def enquiry_type(self):
        if self.trip: return "TRIP_INQUIRY"
        if self.product: return "PRODUCT_ORDER"
        if self.request: return "REQUEST_SUBSCRIPTION"
        return "UNKNOWN"

    def __str__(self):
        return f"{self.enquiry_type} from {self.sender.username}"