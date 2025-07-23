from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Debug summer dress image issue'

    def handle(self, *args, **options):
        try:
            product = Product.objects.get(title='Summer Dress')
            
            self.stdout.write(f'Product ID: {product.id}')
            self.stdout.write(f'Product Title: {product.title}')
            self.stdout.write(f'Product Image Field: {product.image}')
            self.stdout.write(f'Product Image Name: {product.image.name if product.image else "None"}')
            self.stdout.write(f'Product Image URL: {product.image.url if product.image else "None"}')
            
            # Check if image field has a value
            if product.image:
                self.stdout.write(f'Image exists: True')
                self.stdout.write(f'Image path: {product.image.path}')
                
                # Check if physical file exists
                import os
                if os.path.exists(product.image.path):
                    self.stdout.write(f'Physical file exists: True')
                    self.stdout.write(f'File size: {os.path.getsize(product.image.path)} bytes')
                else:
                    self.stdout.write(f'Physical file exists: False')
            else:
                self.stdout.write(f'Image exists: False')
                
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR('Summer Dress product not found'))
