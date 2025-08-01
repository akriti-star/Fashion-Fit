from django.core.management.base import BaseCommand
from products.models import Product
import time


class Command(BaseCommand):
    help = 'Update summer dress to use the new uploaded image'

    def handle(self, *args, **options):
        try:
            product = Product.objects.get(title='Summer Dress')
            old_image = product.image
            
            # Update to use the new image
            product.image = 'products/summer_dress.jpg'
            product.save()
            
            # Add timestamp for cache busting
            timestamp = int(time.time())
            
            self.stdout.write(f'Updated Summer Dress image from: {old_image}')
            self.stdout.write(f'Updated Summer Dress image to: {product.image}')
            self.stdout.write(f'Timestamp for cache busting: {timestamp}')
            self.stdout.write(self.style.SUCCESS('Successfully updated Summer Dress to new uploaded image!'))
            
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR('Summer Dress product not found'))
