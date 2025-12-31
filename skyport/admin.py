from django.contrib import admin
from .models import PassengerTrip, CustomerRequest, Deal

@admin.register(PassengerTrip)
class PassengerTripAdmin(admin.ModelAdmin):
    # What to show in the list view
    list_display = ('traveler', 'origin', 'destination', 'flight_date', 'available_kg', 'is_active', 'created_at')
    
    # How to filter the data in the sidebar
    list_filter = ('is_active', 'flight_date', 'origin', 'destination')
    
    # Which fields can be searched
    search_fields = ('traveler__username', 'origin', 'destination', 'contact_number')
    
    # Grouping the detail view into sections
    fieldsets = (
        ('User Info', {'fields': ('traveler', 'contact_number')}),
        ('Flight Details', {'fields': ('origin', 'destination', 'flight_date', 'available_kg', 'is_active')}),
        ('Pricing Policy', {'fields': ('price_per_kg', 'laptop_fee', 'smartphone_fee')}),
    )

@admin.register(CustomerRequest)
class CustomerRequestAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'sender', 'delivery_destination', 'weight_kg', 'delivery_reward', 'is_purchase_required')
    list_filter = ('is_purchase_required', 'delivery_destination', 'created_at')
    search_fields = ('product_name', 'sender__username', 'pickup_location', 'delivery_destination')
    date_hierarchy = 'created_at'

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('get_product', 'get_traveler', 'get_sender', 'status', 'final_agreed_reward', 'is_paid', 'updated_at')
    list_filter = ('status', 'is_paid')
    search_fields = ('request__product_name', 'trip__traveler__username', 'request__sender__username')
    
    # Custom display methods to show data from linked models
    def get_product(self, obj):
        return obj.request.product_name
    get_product.short_description = 'Product'

    def get_traveler(self, obj):
        return obj.trip.traveler.username
    get_traveler.short_description = 'Traveler'

    def get_sender(self, obj):
        return obj.request.sender.username
    get_sender.short_description = 'Sender'

    # Admin Action: Bulk mark as Paid
    actions = ['mark_as_paid']

    @admin.action(description='Mark selected deals as Paid (Escrow Received)')
    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True)