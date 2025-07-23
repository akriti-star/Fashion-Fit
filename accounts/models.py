from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BODY_TYPE_CHOICES = [
        ('slim', 'Slim'),
        ('average', 'Average'),
        ('curvy', 'Curvy'),
        ('athletic', 'Athletic'),
    ]
    
    USER_TYPE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('both', 'Both'),
    ]
    
    # User role and type
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES, default='buyer')
    
    # Basic info
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    # Body measurements (mainly for buyers)
    height_cm = models.IntegerField(null=True, blank=True, help_text="Height in centimeters")
    weight_kg = models.IntegerField(null=True, blank=True, help_text="Weight in kilograms")
    body_type = models.CharField(max_length=10, choices=BODY_TYPE_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    chest_cm = models.FloatField(null=True, blank=True, help_text="Chest measurement in cm")
    waist_cm = models.FloatField(null=True, blank=True, help_text="Waist measurement in cm")
    hips_cm = models.FloatField(null=True, blank=True, help_text="Hips measurement in cm")
    
    # Seller-specific fields
    business_name = models.CharField(max_length=100, null=True, blank=True)
    business_description = models.TextField(null=True, blank=True)
    tax_id = models.CharField(max_length=50, null=True, blank=True)
    is_verified_seller = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    def get_recommended_size(self):
        """Calculate recommended size based on body measurements"""
        if not self.chest_cm or not self.waist_cm:
            return None
            
        # Simple size recommendation logic
        if self.chest_cm <= 86 and self.waist_cm <= 70:
            return 'XS'
        elif self.chest_cm <= 91 and self.waist_cm <= 75:
            return 'S'
        elif self.chest_cm <= 96 and self.waist_cm <= 80:
            return 'M'
        elif self.chest_cm <= 101 and self.waist_cm <= 85:
            return 'L'
        else:
            return 'XL'
    
    def is_buyer(self):
        return self.user_type in ['buyer', 'both']
    
    def is_seller(self):
        return self.user_type in ['seller', 'both']
    
    def can_sell(self):
        return self.is_seller() and (self.is_verified_seller or not self.is_superuser)
    
    def get_dashboard_url(self):
        """Get the appropriate dashboard URL based on user type"""
        if self.user_type == 'seller':
            return reverse('accounts:seller_dashboard')
        elif self.user_type == 'buyer':
            return reverse('accounts:buyer_dashboard')
        else:  # both
            return reverse('accounts:dashboard_selector')


class UserProfile(models.Model):
    """Extended profile information for users"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    
    # Preferences
    newsletter_subscription = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
