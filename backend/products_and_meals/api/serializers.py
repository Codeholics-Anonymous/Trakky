from rest_framework import serializers
from products_and_meals.models import (Product, Summary, Demand)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'calories_per_hundred_grams', 'protein', 'fat', 'carbohydrates']

class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ['user_id', 'daily_calory_intake', 'date', 'protein', 'fat', 'carbohydrates']

class DemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demand
        fields = ['user_id', 'daily_calory_demand', 'date', 'protein', 'fat', 'carbohydrates']