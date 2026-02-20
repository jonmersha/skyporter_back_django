from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Add phone_number to the forms
    fieldsets = UserAdmin.fieldsets + (
        ('Contact Information', {'fields': ('phone_number',)}),
    )
    # Add phone_number to the creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Contact Information', {'fields': ('phone_number',)}),
    )
    # Fields to display in the list view
    list_display = ['username', 'email', 'phone_number', 'is_staff']
    search_fields = ['username', 'email', 'phone_number']