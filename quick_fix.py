import os
import sys
import django

# Add the project directory to Python path
sys.path.append(r'D:\Python Dev\Python-Fullstack\FashionFit')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashionFit.settings')
django.setup()

from products.models import Product, Category
from accounts.models import CustomUser

print("=== Checking Database Status ===")

# Check existing products
products = Product.objects.all()
print(f"Current products in database: {products.count()}")

if products.count() > 0:
    print("\nExisting products:")
    for product in products:
        print(f"  ID {product.id}: {product.title}")
        print(f"    Try-on URL: http://127.0.0.1:8000/try-on/{product.id}/")
else:
    print("No products found! Creating sample products...")
    
    # Get or create seller
    seller, created = CustomUser.objects.get_or_create(
        username='testselleruser',
        defaults={
            'email': 'testseller@example.com',
            'user_type': 'seller',
            'business_name': 'Test Fashion Store'
        }
    )
    
    if created:
        seller.set_password('testpass123')
        seller.save()
        print(f"Created seller: {seller.username}")
    
    # Get or create category
    category, created = Category.objects.get_or_create(
        slug='tops',
        defaults={'name': 'Tops'}
    )
    
    # Create simple products
    products_data = [
        {'title': 'Blue T-Shirt', 'price': 25.99},
        {'title': 'Red Polo', 'price': 35.99},
        {'title': 'Green Hoodie', 'price': 45.99},
    ]
    
    for i, product_data in enumerate(products_data, 1):
        product = Product.objects.create(
            title=product_data['title'],
            description=f"Test product {i} for virtual try-on",
            price=product_data['price'],
            category=category,
            seller=seller,
            size='M',
            color='Blue',
            is_available=True
        )
        print(f"Created: {product.title} (ID: {product.id})")

print(f"\n=== Final Status ===")
products = Product.objects.all()
print(f"Total products now: {products.count()}")

if products.count() > 0:
    print("\nAvailable try-on URLs:")
    for product in products:
        print(f"  http://127.0.0.1:8000/try-on/{product.id}/ - {product.title}")
    
    print(f"\nTest page: http://127.0.0.1:8000/try-on-test/")
else:
    print("ERROR: Still no products in database!")
