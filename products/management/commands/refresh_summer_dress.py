from django.core.management.base import BaseCommand
from products.models import Product
import time


class Command(BaseCommand):
    help = 'Refresh summer dress image with cache busting'

    def handle(self, *args, **options):
        try:
            product = Product.objects.get(title='Summer Dress')
            
            # Create a new filename with timestamp
            import os
            timestamp = int(time.time())
            
            # Copy the current image to a new timestamped version
            current_image_path = product.image.path
            new_filename = f'products/summer_dress_{timestamp}.jpg'
            new_image_path = os.path.join(
                os.path.dirname(current_image_path),
                f'summer_dress_{timestamp}.jpg'
            )
            
            # Copy the file
            import shutil
            shutil.copy2(current_image_path, new_image_path)
            
            # Update the database
            product.image = new_filename
            product.save()
            
            self.stdout.write(f'Updated Summer Dress image to: {new_filename}')
            self.stdout.write(self.style.SUCCESS('Cache-busting image refresh complete!'))
            
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR('Summer Dress product not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
