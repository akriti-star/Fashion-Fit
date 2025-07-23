import os
import sys
import django

# Add the project directory to sys.path
sys.path.append('d:/Python Dev/Python-Fullstack/FashionFit')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashionFit.settings')
django.setup()

from products.models import Product

print("=== Jacket Product Info ===")
try:
    jacket = Product.objects.get(title='Leather Jacket')
    print(f"Product ID: {jacket.id}")
    print(f"Title: {jacket.title}")
    print(f"Image Field: {jacket.image}")
    print(f"Image URL: {jacket.image.url if jacket.image else 'No image'}")
    print(f"Category: {jacket.category}")
    print(f"Price: ${jacket.price}")
    print(f"Seller: {jacket.seller}")
except Product.DoesNotExist:
    print("Leather Jacket product not found")
    
print("\n=== All Products with 'jacket' in title ===")
jackets = Product.objects.filter(title__icontains='jacket')
for jacket in jackets:
    print(f"- {jacket.title} | Image: {jacket.image}")
