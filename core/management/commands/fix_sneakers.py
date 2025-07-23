from django.core.management.base import BaseCommand
from products.models import Product
from accounts.models import CustomUser
from django.core.files.base import ContentFile
import os


class Command(BaseCommand):
    help = 'Fix running sneakers product with proper image'

    def handle(self, *args, **options):
        self.stdout.write('=== FIXING RUNNING SNEAKERS PRODUCT ===')
        
        # Get or create a seller
        seller = CustomUser.objects.filter(user_type='seller').first()
        if not seller:
            self.stdout.write(self.style.ERROR('No seller account found. Please create a seller first.'))
            return
        
        # Check if running sneakers exists
        sneakers = Product.objects.filter(title__icontains='running sneakers').first()
        
        if sneakers:
            self.stdout.write(f'Found existing product: "{sneakers.title}"')
            
            if not sneakers.image:
                self.stdout.write('Product has no image. Need to upload an image.')
            else:
                # Check if image file exists
                image_path = sneakers.image.path
                if os.path.exists(image_path):
                    self.stdout.write(self.style.SUCCESS('✅ Product and image are properly configured'))
                    self.stdout.write(f'Image URL: {sneakers.image.url}')
                else:
                    self.stdout.write(self.style.ERROR('❌ Image file missing from disk'))
                    self.stdout.write(f'Expected path: {image_path}')
                    
                    # Clear the broken image reference
                    sneakers.image = None
                    sneakers.save()
                    self.stdout.write('Cleared broken image reference')
        else:
            # Create new running sneakers product
            self.stdout.write('Creating new Running Sneakers product...')
            
            sneakers = Product.objects.create(
                title='Running Sneakers',
                description='Comfortable and lightweight running sneakers perfect for daily exercise and sports activities.',
                price=89.99,
                category='shoes',
                seller=seller,
                brand='Athletic Pro',
                size_chart={'XS': 'US 5', 'S': 'US 6-7', 'M': 'US 8-9', 'L': 'US 10-11', 'XL': 'US 12+'}
            )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Created product: "{sneakers.title}"'))
        
        # Instructions for adding image
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('=== NEXT STEPS ==='))
        self.stdout.write('1. Go to your seller dashboard: http://127.0.0.1:8000/accounts/seller/dashboard/')
        self.stdout.write('2. Click "Manage Products"')
        self.stdout.write(f'3. Edit the "{sneakers.title}" product')
        self.stdout.write('4. Upload a proper image file')
        self.stdout.write('5. Save the product')
        self.stdout.write('')
        self.stdout.write('OR use the admin panel to upload an image:')
        self.stdout.write('http://127.0.0.1:8000/admin/products/product/')
        
        self.stdout.write('')
        self.stdout.write(f'Product ID: {sneakers.id}')
        self.stdout.write(f'Seller: {sneakers.seller.username}')
