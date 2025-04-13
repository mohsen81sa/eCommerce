from rest_framework import serializers
from ...models import Product, Category, Brand

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'price', 'discount_price', 'stock', 'category', 'brand', 'status', 'image', 'created_at', 'updated_at', 'is_featured']

    def get_final_price(self, obj):
        return obj.get_final_price()
