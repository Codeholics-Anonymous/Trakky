from rest_framework import serializers
from products_and_meals.models import (Product, Summary, Demand, Meal, MealItem)


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

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['meal_id', 'user_id', 'type', 'date']

class MealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealItem
        fields = ['meal_id', 'product_id', 'gram_amount']