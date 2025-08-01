import os
import sys
import django

# Add the project directory to sys.path
sys.path.append('d:/Python Dev/Python-Fullstack/FashionFit')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashionFit.settings')
django.setup()

from products.models import Product

print("=== Product Images ===")
for product in Product.objects.all():
    print(f"- {product.title}: {product.image}")
