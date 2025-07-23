from django.core.management.base import BaseCommand
from products.models import Product
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Verify cleanup - show only seller-uploaded products'

    def handle(self, *args, **options):
        # Show all products
        products = Product.objects.all()
        self.stdout.write(f'=== DATABASE STATUS ===')
        self.stdout.write(f'Total products in database: {products.count()}')
        
        if products.count() == 0:
            self.stdout.write(self.style.SUCCESS('✅ Database is clean - no products found'))
        else:
            self.stdout.write('')
            self.stdout.write('Products found:')
            for product in products:
                seller_info = f"by {product.seller.username}" if product.seller else "No seller"
                image_info = f"Image: {product.image.name}" if product.image else "No image"
                self.stdout.write(f'- "{product.title}" ({seller_info}) - {image_info}')
        
        # Show sellers
        sellers = CustomUser.objects.filter(user_type='seller')
        self.stdout.write(f'\n=== SELLER ACCOUNTS ===')
        self.stdout.write(f'Total sellers: {sellers.count()}')
        for seller in sellers:
            product_count = Product.objects.filter(seller=seller).count()
            self.stdout.write(f'- {seller.username}: {product_count} products')
        
        self.stdout.write('')
        if products.count() == 0:
            self.stdout.write(self.style.SUCCESS('✅ Ready for sellers to add their own products!'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Some products still exist. Check if they are legitimate seller products.'))
