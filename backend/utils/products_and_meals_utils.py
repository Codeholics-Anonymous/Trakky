from products_and_meals.models import Demand

def find_basic_demand(user_id):
    return Demand.objects.filter(user_id=user_id).order_by('demand_id').first()