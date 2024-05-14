from products_and_meals.models import Demand

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