
from django.db import models
from django.conf import settings
#
class PassengerRate(models.Model):
    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="rates"
    )
    # The name of the item type (e.g., 'Laptop', 'Mobile Phone')
    name = models.CharField(max_length=100) 
    
    # The fee this specific traveler charges for this specific item
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Visual identifiers for the Flutter UI
    icon_identifier = models.CharField(max_length=50, blank=True, help_text="e.g. 'laptop_mac'")
    icon = models.ImageField(upload_to='passenger_icons/', blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)

    class Meta:
        # Ensures a passenger doesn't have duplicate rows for the same item name
        unique_together = ('passenger', 'name')

    def __str__(self):
        return f"{self.passenger.username} - {self.name}: ${self.fee}"
     

# --- Choices ---
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

# --- Models ---

class Trip(models.Model):
    traveler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    departure_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    
    laptop_fee = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    mobile_fee = models.DecimalField(max_digits=10, decimal_places=2, default=30.00)
    cosmetic_fee = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    other_fee = models.DecimalField(max_digits=10, decimal_places=2, default=15.00)
    is_active = models.BooleanField(default=True)

    @property
    def traveler_phone(self):
        return self.traveler.phone_number

    @property
    def traveler_email(self):
        return self.traveler.email

    def __str__(self):
        return f"{self.traveler.username} to {self.destination_city}"


class TravelerProduct(models.Model):
    traveler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listed_products")
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=Category.choices, default=Category.OTHERS)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expected_reward = models.DecimalField(max_digits=10, decimal_places=2)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    expiration_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class ProductImage(models.Model):
    product = models.ForeignKey(TravelerProduct, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

class CustomerRequest(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_requests")
    title = models.CharField(max_length=200)
    request_type = models.CharField(max_length=20, choices=RequestType.choices)
    category = models.CharField(max_length=50, choices=Category.choices)
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    preferred_delivery_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_open = models.BooleanField(default=True)

class Enquiry(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_enquiries")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_enquiries")

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(TravelerProduct, on_delete=models.CASCADE, null=True, blank=True)
    request = models.ForeignKey(CustomerRequest, on_delete=models.CASCADE, null=True, blank=True)

    message = models.TextField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Deal(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buying_deals")
    traveler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="providing_deals")
    
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(TravelerProduct, on_delete=models.SET_NULL, null=True, blank=True)
    request = models.ForeignKey(CustomerRequest, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(max_length=20, choices=DealStatus.choices, default=DealStatus.PENDING)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)