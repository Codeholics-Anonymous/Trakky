from rest_framework import serializers
from products_and_meals.models import (Product, Summary, Demand, Meal, MealItem)
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class ProductSerializer(serializers.ModelSerializer):
    protein = serializers.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    carbohydrates = serializers.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    fat = serializers.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])

    class Meta:
        model = Product
        exclude = ['user_id']

class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = '__all__'

class DemandSerializer(serializers.ModelSerializer):
    protein = serializers.IntegerField(validators=[MaxValueValidator(500), MinValueValidator(0)])
    carbohydrates = serializers.IntegerField(validators=[MaxValueValidator(2000), MinValueValidator(0)])
    fat = serializers.IntegerField(validators=[MaxValueValidator(250), MinValueValidator(0)])

    class Meta:
        model = Demand
        exclude = ['demand_id', 'user_id', 'date']

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

class MealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealItem
        exclude = ['meal_item_id', 'meal_id']