from django.contrib import admin

from .models import Product, Review


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'description', 'sku', 'upc', 'ean', 'mpn', 'category','reviewNumber')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'date', 'platform', 'title', 'text', 'rating')


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
