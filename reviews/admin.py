from django.contrib import admin
from .models import Review, ReviewImage


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating_fit', 'rating_comfort', 'rating_style', 'created_at']
    list_filter = ['rating_fit', 'rating_comfort', 'rating_style', 'created_at']
    search_fields = ['user__username', 'product__title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ReviewImageInline]


admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewImage)
