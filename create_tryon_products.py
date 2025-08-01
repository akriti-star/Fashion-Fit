import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashionFit.settings')
django.setup()

from products.models import Product, Category
from accounts.models import CustomUser
from PIL import Image
import io
from django.core.files.base import ContentFile

print("Creating sample products for try-on testing...")

# Get or create a seller
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
else:
    print(f"Using existing seller: {seller.username}")

# Get or create categories
categories_data = [
    {'name': 'Tops', 'slug': 'tops'},
    {'name': 'Bottoms', 'slug': 'bottoms'},
    {'name': 'Dresses', 'slug': 'dresses'},
    {'name': 'Shoes', 'slug': 'shoes'},
]

categories = {}
for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={'name': cat_data['name']}
    )
    categories[cat_data['slug']] = cat

# Create sample products for try-on
products_data = [
    {
        'title': 'Myntra Style T-Shirt',
        'description': 'Comfortable cotton t-shirt perfect for virtual try-on testing',
        'price': 25.99,
        'category': categories['tops'],
        'size': 'M',
        'color': 'Blue',
    },
    {
        'title': 'Classic Jeans',
        'description': 'Premium denim jeans for virtual fitting',
        'price': 79.99,
        'category': categories['bottoms'],
        'size': 'L',
        'color': 'Dark Blue',
    },
    {
        'title': 'Summer Dress',
        'description': 'Light and airy summer dress',
        'price': 59.99,
        'category': categories['dresses'],
        'size': 'S',
        'color': 'Floral',
    },
    {
        'title': 'Casual Sneakers',
        'description': 'Comfortable sneakers for everyday wear',
        'price': 89.99,
        'category': categories['shoes'],
        'size': '9',
        'color': 'White',
    },
]

created_products = []
for product_data in products_data:
    # Check if product already exists
    existing = Product.objects.filter(title=product_data['title']).first()
    if existing:
        print(f"Product already exists: {existing.title}")
        created_products.append(existing)
        continue
    
    # Create a simple colored image
    img = Image.new('RGB', (400, 600), color='lightblue')
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG', quality=85)
    img_io.seek(0)
    
    # Create product
    product = Product.objects.create(
        title=product_data['title'],
        description=product_data['description'],
        price=product_data['price'],
        category=product_data['category'],
        seller=seller,
        size=product_data['size'],
        color=product_data['color'],
        is_available=True
    )
    
    # Add image
    product.image.save(
        f'{product.title.lower().replace(" ", "_")}.jpg',
        ContentFile(img_io.getvalue()),
        save=True
    )
    
    created_products.append(product)
    print(f"Created product: {product.title} (ID: {product.id})")

print(f"\nTotal products available: {Product.objects.count()}")
print(f"Created/verified {len(created_products)} products for try-on testing")

print("\n=== Try-On URLs ===")
for product in created_products:
    print(f"- {product.title}: http://127.0.0.1:8000/try-on/{product.id}/")

print(f"\n=== Test Page URL ===")
print("http://127.0.0.1:8000/try-on-test/")
