from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Outfit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='OutfitProduct')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} by {self.user.username}"
    
    def get_total_price(self):
        return sum(product.price for product in self.products.all())


class OutfitProduct(models.Model):
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['outfit', 'product']
    
    def __str__(self):
        return f"{self.product.title} in {self.outfit.name}"


class OutfitLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'outfit']
    
    def __str__(self):
        return f"{self.user.username} likes {self.outfit.name}"
