from products_and_meals.models import Demand, Meal, MealItem
from django.db.models import Q

def find_first_demand(userprofile_id):
    return Demand.objects.filter(userprofile_id=userprofile_id).order_by('demand_id').first()

# check if sum of args isn't larger than limit
def above_upper_limit(*args, limit):
    sum = 0
    for x in args:
        sum += x
    if sum > limit:
        return True
    else:
        return False

# return queryset of all mealitems found at meal at selected date
def find_mealitems(user_id, product_id, date):
    # firstly - find all meals from that date
    meals = Meal.objects.filter(user_id=user_id, date=date)
    meals_id = (x.meal_id for x in meals)
    # create query to find all mealitems with above meal_id
    query = Q()
    for x in meals_id:
        query = Q(meal_id=x) | query
    # find all mealitems
    mealitems = MealItem.objects.filter(query, product_id=product_id)
    return mealitems

# calculate macros for basic demand
def basic_macros(demand):
    # 50/20/30 - 50% carbohydrates, 20% protein, 30% fat
    protein = round(((0.2*demand) / 4), 1)
    carbohydrates = round(((0.5*demand) / 4), 1)
    fat = round(((0.3*demand) / 9), 1)
    return (protein, carbohydrates, fat)

from products_and_meals.api.serializers import ProductSerializer
from products_and_meals.models import Product
from utils.responses import custom_response
from rest_framework.response import Response
from rest_framework import status

def add_product(request_data, user_id):
    serializer = ProductSerializer(data=request_data)
    if serializer.is_valid():
        # check if this product exists in database
        if Product.objects.filter(name=serializer.validated_data['name']).exists():
            return custom_response("Product", "already exists")
        # check if sum of macros isn't larger than 100g
        if above_upper_limit(serializer.validated_data['protein'], serializer.validated_data['carbohydrates'], serializer.validated_data['fat'], limit=100):
            return custom_response("Macros", f"amount to high ({serializer.validated_data['protein'] + serializer.validated_data['carbohydrates'] + serializer.validated_data['fat']}/{100})", status.HTTP_400_BAD_REQUEST)
        # add product
        added_product = Product.add_product(
            user_id=user_id,
            name=serializer.validated_data['name'],
            protein=serializer.validated_data['protein'],
            carbohydrates=serializer.validated_data['carbohydrates'],
            fat=serializer.validated_data['fat'],
        )
        data = serializer.validated_data|{'calories_per_hundred_grams' : added_product.calories_per_hundred_grams}
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)