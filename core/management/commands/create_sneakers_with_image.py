from django.core.management.base import BaseCommand
from products.models import Product
from accounts.models import CustomUser
from django.core.files.base import ContentFile
from PIL import Image
import io
import os


class Command(BaseCommand):
    help = 'Create running sneakers with a working placeholder image'

    def handle(self, *args, **options):
        self.stdout.write('=== CREATING RUNNING SNEAKERS WITH PLACEHOLDER ===')
        
        # Get or create seller
        seller = CustomUser.objects.filter(user_type='seller').first()
        if not seller:
            # Create a test seller if none exists
            seller = CustomUser.objects.create_user(
                username='testseller',
                email='seller@test.com',
                password='testpass123',
                user_type='seller',
                business_name='Test Fashion Store',
                is_verified_seller=True
            )
            self.stdout.write(f'Created test seller: {seller.username}')
        
        # Delete existing running sneakers if any
        existing = Product.objects.filter(title__icontains='running sneakers')
        if existing.exists():
            self.stdout.write(f'Deleting {existing.count()} existing sneakers products')
            existing.delete()
        
        # Create placeholder image
        self.stdout.write('Creating placeholder image...')
        img = Image.new('RGB', (400, 400), color='lightblue')
        
        # Add some text to the image
        try:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            
            # Try to use a default font
            try:
                font = ImageFont.truetype('arial.ttf', 24)
            except:
                font = ImageFont.load_default()
            
            # Add text
            text = 'Running Sneakers'
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (400 - text_width) // 2
            y = (400 - text_height) // 2
            
            draw.text((x, y), text, fill='white', font=font)
            draw.text((x, y + 30), 'Placeholder Image', fill='white', font=font)
            
        except Exception as e:
            self.stdout.write(f'Could not add text to image: {e}')
        
        # Save image to BytesIO
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        
        # Create the product
        product = Product.objects.create(
            title='Running Sneakers',
            description='High-quality running sneakers perfect for daily exercise, jogging, and sports activities. Comfortable cushioning and breathable material.',
            price=89.99,
            category='shoes',
            seller=seller,
            brand='Athletic Pro',
            size_chart={
                'XS': 'US 5-5.5',
                'S': 'US 6-7',
                'M': 'US 8-9',
                'L': 'US 10-11',
                'XL': 'US 12+'
            }
        )
        
        # Save the image
        image_file = ContentFile(img_io.getvalue(), name='running_sneakers_placeholder.jpg')
        product.image.save('running_sneakers_placeholder.jpg', image_file, save=True)
        
        self.stdout.write(self.style.SUCCESS(f'✅ Created product: \"{product.title}\"'))
        self.stdout.write(f'Product ID: {product.id}')
        self.stdout.write(f'Image: {product.image.name}')
        self.stdout.write(f'Image URL: {product.image.url}')
        self.stdout.write(f'Image path: {product.image.path}')
        
        # Verify file exists
        if os.path.exists(product.image.path):
            size = os.path.getsize(product.image.path)
            self.stdout.write(self.style.SUCCESS(f'✅ Image file created successfully ({size} bytes)'))
        else:
            self.stdout.write(self.style.ERROR('❌ Image file was not created'))
        
        self.stdout.write('')
        self.stdout.write('The product should now be visible on:')
        self.stdout.write('- Home page: http://127.0.0.1:8000/')
        self.stdout.write('- Products page: http://127.0.0.1:8000/products/')
        self.stdout.write(f'- Product detail: http://127.0.0.1:8000/products/{product.id}/')
        self.stdout.write('')
        self.stdout.write('To replace with a real image:')
        self.stdout.write('1. Go to seller dashboard: http://127.0.0.1:8000/accounts/seller/dashboard/')
        self.stdout.write('2. Edit the product and upload a new image')
