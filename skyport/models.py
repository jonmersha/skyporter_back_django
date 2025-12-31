from django.db import models
from django.conf import settings

# Status choices for the Deal workflow
class DealStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending Agreement'
    ACCEPTED = 'ACCEPTED', 'Deal Accepted'
    PURCHASED = 'PURCHASED', 'Item Purchased'
    IN_TRANSIT = 'IN_TRANSIT', 'In Transit'
    ARRIVED = 'ARRIVED', 'Arrived at Destination'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'

class PassengerTrip(models.Model):
    """Model for Travelers offering luggage space"""
    traveler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trips')
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    flight_date = models.DateField()
    available_kg = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Pricing Policy
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    laptop_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    smartphone_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    contact_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.traveler.username}: {self.origin} to {self.destination}"

class CustomerRequest(models.Model):
    """Model for Senders requesting an item to be delivered"""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests')
    product_name = models.CharField(max_length=200)
    pickup_location = models.CharField(max_length=100)
    delivery_destination = models.CharField(max_length=100)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Item Details
    is_purchase_required = models.BooleanField(default=False)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    delivery_reward = models.DecimalField(max_digits=10, decimal_places=2)
    
    contact_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} to {self.delivery_destination}"

class Deal(models.Model):
    """Model connecting a Trip and a Request into a formal agreement"""
    request = models.OneToOneField(CustomerRequest, on_delete=models.CASCADE, related_name='deal')
    trip = models.ForeignKey(PassengerTrip, on_delete=models.CASCADE, related_name='deals')
    
    # Status and Escrow
    status = models.CharField(
        max_length=20, 
        choices=DealStatus.choices, 
        default=DealStatus.PENDING
    )
    final_agreed_reward = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False) # True when customer pays escrow
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Deal: {self.request.product_name} ({self.status})"