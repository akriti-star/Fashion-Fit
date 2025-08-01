import os
import sys
import django

# Add the project directory to sys.path
sys.path.append('d:/Python Dev/Python-Fullstack/FashionFit')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashionFit.settings')
django.setup()

from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

print("=== Database Status ===")
print(f"Total products: {Product.objects.count()}")
print(f"Products with sellers: {Product.objects.filter(seller__isnull=False).count()}")
print(f"Total users: {User.objects.count()}")
print(f"Total sellers: {User.objects.filter(user_type__in=['seller', 'both']).count()}")

print("\n=== Product Details ===")
for product in Product.objects.all()[:5]:
    print(f"- {product.title} | Seller: {product.seller.username if product.seller else 'None'}")

print("\n=== User Details ===")
for user in User.objects.all():
    print(f"- {user.username} | Type: {user.user_type} | Superuser: {user.is_superuser}")
