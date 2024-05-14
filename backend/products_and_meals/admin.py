from django.contrib import admin
from .models import (Macros, Product, Demand, Summary, Meal, MealItem)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'user_id', 'name', 'calories_per_hundred_grams', 'protein', 'fat', 'carbohydrates')

@admin.register(Demand)
class DemandAdmin(admin.ModelAdmin):
    list_display = ('demand_id', 'user_id', 'date', 'protein', 'carbohydrates', 'fat','daily_calory_demand')

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('summary_id', 'user_id', 'date', 'daily_calory_intake')

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('meal_id', 'user_id', 'type', 'date')

@admin.register(MealItem)
class MealItemAdmin(admin.ModelAdmin):
    list_display = ('meal_item_id', 'meal_id', 'product_id', 'gram_amount')