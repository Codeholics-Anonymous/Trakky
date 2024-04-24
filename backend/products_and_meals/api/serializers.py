from rest_framework import serializers
from products_and_meals.models import Product


class ProductSerializer():
    class Meta:
        model = Product
        fields = ['productID', 'name', 'caloriesPerHundredGrams']