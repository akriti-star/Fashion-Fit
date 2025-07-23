import os
import sys
import django

# Add the project directory to sys.path
sys.path.append('d:/Python Dev/Python-Fullstack/FashionFit')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashionFit.settings')
django.setup()

from products.models import Product

summer_dress = Product.objects.get(title='Summer Dress')
print(f"Summer Dress ID: {summer_dress.id}")
print(f"Summer Dress Image: {summer_dress.image}")
print(f"Summer Dress Image URL: {summer_dress.image.url if summer_dress.image else 'No image'}")
print(f"Direct URL: http://127.0.0.1:8000{summer_dress.image.url if summer_dress.image else '/no-image'}")
