from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Product, SizeChart
from decimal import Decimal
import os
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample data and create placeholder images'

    def create_placeholder_image(self, product_title, category, filename):
        """Create a placeholder image for a product"""
        # Create a colored background based on category
        colors = {
            'top': '#E3F2FD',      # Light blue
            'bottom': '#F3E5F5',   # Light purple
            'dress': '#FCE4EC',    # Light pink
            'outerwear': '#E8F5E8', # Light green
            'shoes': '#FFF3E0',    # Light orange
            'accessories': '#F1F8E9', # Light lime
        }
        
        bg_color = colors.get(category, '#F5F5F5')
        
        # Create image
        img = Image.new('RGB', (400, 500), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a default font
        try:
            font = ImageFont.truetype("arial.ttf", 24)
            small_font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Draw product title
        try:
            text_width = draw.textlength(product_title, font=font)
        except:
            text_width = len(product_title) * 12  # Fallback
        text_x = max(10, (400 - text_width) // 2)
        draw.text((text_x, 200), product_title, fill='#333333', font=font)
        
        # Draw category
        cat_text = category.upper()
        try:
            cat_width = draw.textlength(cat_text, font=small_font)
        except:
            cat_width = len(cat_text) * 8  # Fallback
        cat_x = max(10, (400 - cat_width) // 2)
        draw.text((cat_x, 240), cat_text, fill='#666666', font=small_font)
        
        # Draw placeholder text
        placeholder_text = "PLACEHOLDER IMAGE"
        try:
            placeholder_width = draw.textlength(placeholder_text, font=small_font)
        except:
            placeholder_width = len(placeholder_text) * 8  # Fallback
        placeholder_x = max(10, (400 - placeholder_width) // 2)
        draw.text((placeholder_x, 300), placeholder_text, fill='#999999', font=small_font)
        
        # Save image
        media_path = os.path.join(settings.MEDIA_ROOT, 'products')
        os.makedirs(media_path, exist_ok=True)
        img.save(os.path.join(media_path, filename))

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create size charts
        size_charts = [
            {
                'xs_chest': 32, 'xs_waist': 24, 'xs_hip': 34,
                's_chest': 34, 's_waist': 26, 's_hip': 36,
                'm_chest': 36, 'm_waist': 28, 'm_hip': 38,
                'l_chest': 38, 'l_waist': 30, 'l_hip': 40,
                'xl_chest': 40, 'xl_waist': 32, 'xl_hip': 42,
            }
        ]
        
        # Create or get the default size chart
        size_chart, created = SizeChart.objects.get_or_create(
            id=1,
            defaults=size_charts[0]
        )
        if created:
            self.stdout.write('Created default size chart')
        
        # Create sample products with images
        products = [
            {
                'title': 'Classic White T-Shirt',
                'category': 'top',
                'description': 'A comfortable and versatile white t-shirt made from 100% cotton.',
                'price': Decimal('19.99'),
                'image': 'products/classic_white_tshirt.jpg',
            },
            {
                'title': 'Slim Fit Jeans',
                'category': 'bottom',
                'description': 'Modern slim-fit jeans with a comfortable stretch.',
                'price': Decimal('59.99'),
                'image': 'products/slim_fit_jeans.jpg',
            },
            {
                'title': 'Summer Dress',
                'category': 'dress',
                'description': 'Light and airy summer dress perfect for warm weather.',
                'price': Decimal('45.99'),
                'image': 'products/summer_dress.jpg',
            },
            {
                'title': 'Leather Jacket',
                'category': 'outerwear',
                'description': 'Premium leather jacket with classic styling.',
                'price': Decimal('149.99'),
                'image': 'products/leather_jacket.jpg',
            },
            {
                'title': 'Running Shoes',
                'category': 'shoes',
                'description': 'Comfortable running shoes with excellent support.',
                'price': Decimal('89.99'),
                'image': 'products/running_shoes.jpg',
            },
            {
                'title': 'Designer Handbag',
                'category': 'accessories',
                'description': 'Elegant handbag perfect for any occasion.',
                'price': Decimal('79.99'),
                'image': 'products/designer_handbag.jpg',
            },
        ]
        
        for product_data in products:
            product, created = Product.objects.get_or_create(
                title=product_data['title'],
                defaults=product_data
            )
            if created:
                # Assign size chart
                product.size_chart = size_chart
                product.save()
                
                # Create placeholder image
                image_filename = os.path.basename(product_data['image'])
                self.create_placeholder_image(
                    product.title, 
                    product.category, 
                    image_filename
                )
                
                self.stdout.write(f'Created product: {product.title} with image')
        
        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@fashionfit.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Created superuser: admin (password: admin123)'))
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
