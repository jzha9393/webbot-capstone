from rest_framework import serializers
from .models import Product, Review



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ['id','name', 'description', 'brand', 'category', 'SKU', 'UPC', 'EAN', 'MPN']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        # fields = ['id','user', 'platform', 'date', 'title','text','rating','product_FK_id']


