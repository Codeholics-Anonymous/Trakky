from rest_framework import serializers
from products_and_meals.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'calories_per_hundred_grams', 'protein', 'fat', 'carbohydrates']