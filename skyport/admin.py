from django.contrib import admin
from .models import (
    Trip, TravelerProduct, ProductImage, 
    CustomerRequest, Deal, Enquiry
)

# 1. Product Image Inline
# This allows you to upload multiple images directly on the TravelerProduct page
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# 2. Trip Admin
@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('destination_city', 'traveler', 'arrival_date', 'laptop_fee', 'mobile_fee', 'is_active')
    list_filter = ('destination_city', 'is_active', 'arrival_date')
    search_fields = ('traveler__username', 'destination_city', 'departure_city')
    list_editable = ('is_active',)

# 3. Traveler Product Admin
@admin.register(TravelerProduct)
class TravelerProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'traveler', 'category', 'price', 'expected_reward', 'arrival_date')
    list_filter = ('category', 'arrival_date')
    search_fields = ('name', 'traveler__username', 'description')
    inlines = [ProductImageInline]

# 4. Customer Request Admin
@admin.register(CustomerRequest)
class CustomerRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'request_type', 'category', 'to_city', 'is_open')
    list_filter = ('request_type', 'category', 'is_open')
    search_fields = ('title', 'customer__username', 'to_city')

# 5. Enquiry Admin (Communication logs)
@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'enquiry_type', 'is_accepted', 'created_at')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'message')
    readonly_fields = ('created_at',)

# 6. Deal Admin (The Transaction Hub)
@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'traveler', 'status', 'final_price', 'updated_at')
    list_filter = ('status', 'updated_at')
    search_fields = ('customer__username', 'traveler__username', 'id')
    list_editable = ('status',)
    
    fieldsets = (
        ('Parties', {
            'fields': ('customer', 'traveler')
        }),
        ('Sources', {
            'description': "Only one of these will typically be linked.",
            'fields': ('trip', 'product', 'request')
        }),
        ('Status & Pricing', {
            'fields': ('status', 'final_price')
        }),
    )