#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashionFit.settings')
django.setup()

from products.models import Product
from accounts.models import CustomUser
from django.urls import reverse

print("=== FashionFit Virtual Try-On Status Check ===\n")

# Check products
products = Product.objects.all()
print(f"Total products in database: {products.count()}")

if products.count() > 0:
    print("\nAvailable products for try-on:")
    for product in products[:5]:
        try_on_url = f"/try-on/{product.id}/"
        print(f"- {product.name} (ID: {product.id})")
        print(f"  Try-on URL: {try_on_url}")
        print(f"  Product URL: /products/{product.id}/")
        print()
else:
    print("No products found in database!")

# Check users
users = CustomUser.objects.all()
print(f"Total users: {users.count()}")

if users.count() > 0:
    print("\nUsers with body measurements:")
    for user in users:
        if user.height_cm or user.weight_kg:
            print(f"- {user.username}: Height: {user.height_cm}cm, Weight: {user.weight_kg}kg")

print("\n=== URL Patterns Available ===")
print("- Home: /")
print("- Try-on test page: /try-on-test/")
print("- Product try-on: /try-on/<product_id>/")
print("- Products list: /products/")

print("\n=== Next Steps ===")
print("1. Start server with: python manage.py runserver")
print("2. Visit: http://127.0.0.1:8000/try-on-test/")
print("3. Check products at: http://127.0.0.1:8000/products/")
print("4. Try virtual try-on from any product detail page")
