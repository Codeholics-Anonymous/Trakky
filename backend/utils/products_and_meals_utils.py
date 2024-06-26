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