from products_and_meals.models import Demand, Meal, MealItem
from django.db.models import Q

def find_basic_demand(user_id):
    return Demand.objects.filter(user_id=user_id).order_by('demand_id').first()

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