from rest_framework import serializers
from store.models import Product, Category
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'products_count']

    products_count = serializers.SerializerMethodField(method_name='get_products_count')

    def get_products_count(self, category: Category):
        return category.products.count()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'price_with_tax', 'category']

    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')
    category = CategorySerializer()

    def get_price_with_tax(self, product: Product):
        return product.price * Decimal(1.1)
