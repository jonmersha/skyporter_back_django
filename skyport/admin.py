from django.contrib import admin
from .models import Trip, TravelerProduct, ProductImage, CustomerRequest, Enquiry, Deal

# --- Inlines ---
# This allows you to upload multiple images directly on the TravelerProduct page
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty image slots to show by default

# --- Model Admin Classes ---

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('traveler', 'departure_city', 'destination_city', 'arrival_date', 'is_active')
    list_filter = ('is_active', 'arrival_date', 'destination_city')
    search_fields = ('traveler__username', 'departure_city', 'destination_city')
    ordering = ('-arrival_date',)
    # Organizing the fee structure in a specific section
    fieldsets = (
        (None, {'fields': ('traveler', 'is_active')}),
        ('Travel Info', {'fields': ('departure_city', 'destination_city', 'arrival_date')}),
        ('Fee Structure', {
            'fields': ('laptop_fee', 'mobile_fee', 'cosmetic_fee', 'other_fee'),
            'description': 'Set the standard pricing for this specific trip.'
        }),
    )

@admin.register(TravelerProduct)
class TravelerProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'traveler', 'category', 'price', 'arrival_date', 'created_at')
    list_filter = ('category', 'arrival_date')
    search_fields = ('name', 'traveler__username', 'description')
    inlines = [ProductImageInline]  # Attach images here
    date_hierarchy = 'arrival_date'

@admin.register(CustomerRequest)
class CustomerRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'request_type', 'category', 'to_city', 'is_open')
    list_filter = ('request_type', 'category', 'is_open')
    search_fields = ('title', 'customer__username', 'from_city', 'to_city')

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'is_accepted', 'created_at')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'message')
    readonly_fields = ('created_at',) # Prevent manual editing of timestamps

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'traveler', 'status', 'final_price', 'updated_at')
    list_editable = ('status',)  # Change deal status directly from the list view!
    list_filter = ('status', 'updated_at')
    search_fields = ('customer__username', 'traveler__username', 'id')
    readonly_fields = ('updated_at',)

    def get_queryset(self, request):
        # Optimization: Fetch foreign keys in one query
        return super().get_queryset(request).select_related('customer', 'traveler')