#!/usr/bin/env python
import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashionFit.settings')
django.setup()

from accounts.models import CustomUser

# Create a seller account
seller_username = 'testseller'
seller_email = 'seller@test.com'
seller_password = 'seller123'

# Check if seller already exists
if CustomUser.objects.filter(username=seller_username).exists():
    print(f"Seller account '{seller_username}' already exists!")
    seller = CustomUser.objects.get(username=seller_username)
else:
    # Create seller account
    seller = CustomUser.objects.create_user(
        username=seller_username,
        email=seller_email,
        password=seller_password,
        user_type='seller',
        first_name='Test',
        last_name='Seller',
        is_verified_seller=True  # Make them verified so they can sell
    )
    print(f"Created seller account: {seller_username}")

print(f"Seller details:")
print(f"  Username: {seller.username}")
print(f"  Email: {seller.email}")
print(f"  User type: {seller.user_type}")
print(f"  Is seller: {seller.is_seller()}")
print(f"  Can sell: {seller.can_sell()}")
print(f"  Is verified: {seller.is_verified_seller}")
print(f"\nYou can now login as: {seller_username} / {seller_password}")
