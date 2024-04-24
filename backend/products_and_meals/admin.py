from django.contrib import admin
from .models import Macros, Product,Demand,Summary

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'calories_per_hundred_grams', 'protein', 'fat', 'carbohydrates')
@admin.register(Demand)
class DemandAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'date', 'protein', 'carbohydrates', 'fat','daily_calory_demand')

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'date', 'daily_calory_intake')