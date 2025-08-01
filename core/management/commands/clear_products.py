from django.core.management.base import BaseCommand
from products.models import Product
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Clear all existing products and their images'

    def handle(self, *args, **options):
        # Get all products
        products = Product.objects.all()
        
        self.stdout.write(f"Found {products.count()} products to delete")
        
        # Delete product images from filesystem
        deleted_images = 0
        for product in products:
            if product.image:
                image_path = os.path.join(settings.MEDIA_ROOT, str(product.image))
                if os.path.exists(image_path):
                    try:
                        os.remove(image_path)
                        deleted_images += 1
                        self.stdout.write(f"Deleted image: {image_path}")
                    except Exception as e:
                        self.stdout.write(f"Error deleting image {image_path}: {str(e)}")
        
        # Delete all products from database
        deleted_count = products.count()
        products.delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {deleted_count} products and {deleted_images} images')
        )
        self.stdout.write(
            self.style.SUCCESS('You can now add products from the seller dashboard at /products/seller/')
        )
