#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashionFit.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

def create_test_users():
    """Create test users for testing role-based functionality"""
    
    try:
        with transaction.atomic():
            # Create a regular user (non-superuser)
            regular_user, created = User.objects.get_or_create(
                username='testuser',
                defaults={
                    'email': 'test@example.com',
                    'first_name': 'Test',
                    'last_name': 'User',
                    'is_superuser': False,
                    'is_staff': False,
                    'gender': 'M',
                    'body_type': 'average',
                    'height_cm': 175,
                    'weight_kg': 70,
                    'chest_cm': 90.0,
                    'waist_cm': 75.0,
                    'hips_cm': 85.0,
                }
            )
            
            if created:
                regular_user.set_password('testpass123')
                regular_user.save()
                print(f"✓ Created regular user: {regular_user.username}")
            else:
                print(f"✓ Regular user already exists: {regular_user.username}")
            
            # Create a superuser
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@example.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'is_superuser': True,
                    'is_staff': True,
                    'gender': 'F',
                    'body_type': 'slim',
                    'height_cm': 165,
                    'weight_kg': 55,
                    'chest_cm': 85.0,
                    'waist_cm': 68.0,
                    'hips_cm': 90.0,
                }
            )
            
            if created:
                admin_user.set_password('admin123')
                admin_user.save()
                print(f"✓ Created admin user: {admin_user.username}")
            else:
                print(f"✓ Admin user already exists: {admin_user.username}")
                
            print("\n=== Test Users Created Successfully ===")
            print("Regular User - Username: testuser, Password: testpass123")
            print("Admin User - Username: admin, Password: admin123")
            print("\nYou can now test the role-based logout functionality:")
            print("1. Login as 'testuser' - logout should redirect to home page")
            print("2. Login as 'admin' - logout should redirect to admin panel")
            
    except Exception as e:
        print(f"Error creating test users: {e}")

if __name__ == '__main__':
    create_test_users()
