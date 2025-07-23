from django.contrib import admin
from .models import Outfit, OutfitProduct, OutfitLike


class OutfitProductInline(admin.TabularInline):
    model = OutfitProduct
    extra = 1


class OutfitAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OutfitProductInline]


class OutfitLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'outfit', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'outfit__name']


admin.site.register(Outfit, OutfitAdmin)
admin.site.register(OutfitLike, OutfitLikeAdmin)
