from django.contrib import admin
from .models import Macros, Product

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'calories_per_hundred_grams', 'protein', 'fat', 'carbohydrates')
