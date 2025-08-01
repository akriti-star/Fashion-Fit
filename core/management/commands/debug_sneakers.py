from django.core.management.base import BaseCommand
from products.models import Product
from accounts.models import CustomUser
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Debug running sneakers image issue'

    def handle(self, *args, **options):
        self.stdout.write('=== DEBUGGING RUNNING SNEAKERS ===')
        
        # Search for running sneakers (case insensitive)
        sneakers_products = Product.objects.filter(title__icontains='sneakers')
        
        if not sneakers_products.exists():
            self.stdout.write(self.style.WARNING('No sneakers products found in database'))
            
            # Check if we need to create one for testing
            sellers = CustomUser.objects.filter(user_type='seller')
            if sellers.exists():
                seller = sellers.first()
                self.stdout.write(f'Found seller: {seller.username}')
                self.stdout.write('Would you like me to create a test running sneakers product? (This is just for debugging)')
            else:
                self.stdout.write(self.style.ERROR('No sellers found to create test product'))
        else:
            self.stdout.write(f'Found {sneakers_products.count()} sneakers product(s):')
            
            for product in sneakers_products:
                self.stdout.write(f'\n--- Product: "{product.title}" ---')
                self.stdout.write(f'ID: {product.id}')
                self.stdout.write(f'Seller: {product.seller.username if product.seller else "None"}')
                self.stdout.write(f'Price: ${product.price}')
                self.stdout.write(f'Category: {product.category}')
                
                if product.image:
                    self.stdout.write(f'Image field: {product.image}')
                    self.stdout.write(f'Image name: {product.image.name}')
                    self.stdout.write(f'Image URL: {product.image.url}')
                    
                    # Check if file exists
                    full_path = os.path.join(settings.MEDIA_ROOT, product.image.name)
                    self.stdout.write(f'Full path: {full_path}')
                    
                    if os.path.exists(full_path):
                        file_size = os.path.getsize(full_path)
                        self.stdout.write(self.style.SUCCESS(f'✅ File exists ({file_size} bytes)'))
                    else:
                        self.stdout.write(self.style.ERROR('❌ Image file missing from disk'))
                        self.stdout.write('This is likely why the image is not displaying')
                else:
                    self.stdout.write(self.style.WARNING('❌ No image uploaded for this product'))
        
        # Show all products for context
        self.stdout.write('\n=== ALL PRODUCTS IN DATABASE ===')
        all_products = Product.objects.all()
        
        if all_products.exists():
            for product in all_products:
                image_status = "✅ Has image" if product.image else "❌ No image"
                self.stdout.write(f'- "{product.title}" | {image_status}')
        else:
            self.stdout.write('No products in database')
        
        # Check media directory
        self.stdout.write('\n=== MEDIA DIRECTORY STATUS ===')
        media_products_path = os.path.join(settings.MEDIA_ROOT, 'products')
        
        if os.path.exists(media_products_path):
            files = os.listdir(media_products_path)
            if files:
                self.stdout.write('Files in media/products:')
                for file in files:
                    file_path = os.path.join(media_products_path, file)
                    if os.path.isfile(file_path):
                        size = os.path.getsize(file_path)
                        self.stdout.write(f'- {file} ({size} bytes)')
            else:
                self.stdout.write('Media/products directory is empty')
        else:
            self.stdout.write('Media/products directory does not exist')
