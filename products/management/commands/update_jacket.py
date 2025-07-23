from django.core.management.base import BaseCommand
from products.models import Product
import time


class Command(BaseCommand):
    help = 'Update leather jacket image'

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, help='New image filename (e.g., leather_jacket_new.jpg)')

    def handle(self, *args, **options):
        try:
            product = Product.objects.get(title='Leather Jacket')
            old_image = product.image
            
            # Use provided filename or default
            new_filename = options.get('filename', 'leather_jacket.jpg')
            
            # Update the image
            product.image = f'products/{new_filename}'
            product.save()
            
            self.stdout.write(f'Updated Leather Jacket image from: {old_image}')
            self.stdout.write(f'Updated Leather Jacket image to: {product.image}')
            self.stdout.write(self.style.SUCCESS('Successfully updated Leather Jacket image!'))
            
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR('Leather Jacket product not found'))
