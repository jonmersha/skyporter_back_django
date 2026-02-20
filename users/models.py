from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Add contact fields directly to the User model
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=20, 
        help_text="Enter with country code, e.g., 251911223344",
        blank=True, 
        null=True
    )
