from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from products_and_meals.models import (Product, Summary, Demand, Meal, MealItem)
from products_and_meals.api.serializers import (ProductSerializer, SummarySerializer, DemandSerializer, MealSerializer, MealItemSerializer)
from datetime import datetime, date

# PRODUCT VIEWS

@api_view(['GET'])
def api_detail_product_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['PUT'])
def api_update_product_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        data = {}
        if serializer.is_valid():
            Product.update_product(
                product_id, 
                serializer.validated_data['name'], 
                serializer.validated_data['protein'],
                serializer.validated_data['fat'],
                serializer.validated_data['carbohydrates'],
                serializer.validated_data['calories_per_hundred_grams']
                )
            data["success"] = "update successful"
            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'],)
def api_delete_product_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = product.delete()
        data = {}
        if operation:
            data["success"] = "deletion successful"
        else:
            data["failure"] = "deletion failed"
        return Response(data=data)

@api_view(['POST'])
def api_create_product_view(request):
    #account = request.user #when we will have users authentication it will work

    product = Product()

    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        added_product = Product.add_product(
            name=serializer.validated_data['name'],
            protein=serializer.validated_data['protein'],
            carbohydrates=serializer.validated_data['carbohydrates'],
            fat=serializer.validated_data['fat'],
        )
        data = serializer.validated_data|{'calories_per_hundred_grams' : added_product.calories_per_hundred_grams}
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# SUMMARY VIEWS

# we only need GET request because other changes are caused by mealitem and meal classes

@api_view(['GET'])
def api_detail_summary_view(request, user_id, date):
    try:
        summary = Summary.objects.get(user_id=user_id, date=date)
    except Summary.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SummarySerializer(summary, many=True)
        return Response(serializer.data)

@api_view(['DELETE'])
def api_delete_summary_view():
    ...

# DEMAND VIEWS

@api_view(['GET'])
def api_detail_demand_view(request, user_id, date):
    demand = Demand.objects.filter(user_id=user_id, date__lte=date).order_by('-date').first()
    if demand is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = DemandSerializer(demand)
    return Response(serializer.data)        

@api_view(['POST'])
def api_create_demand_view(request):
    
    user_id = request.user.id
    serializer = DemandSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # check if enough data was provided to calculate demand

    only_demand = ( # check if only demand is given
        (serializer.data['fat'] is None or serializer.data['fat'] == 0) 
        and 
        (serializer.data['protein'] is None or serializer.data['protein'] == 0) 
        and 
        (serializer.data['carbohydrates'] is None or serializer.data['carbohydrates'] == 0)) 
    
    if (only_demand and (serializer.data['daily_calory_demand'] is None or serializer.data['daily_calory_demand'] == 0)):
        return Response({'information' : 'not provided'}, status=status.HTTP_400_BAD_REQUEST)

    # check if we have actually demand from today in database

    if not Demand.objects.get(user_id=user_id, date=date.today()):
        demand = Demand(user_id=user_id, date=date.today(), protein=0, fat=0, carbohydrates=0, daily_calory_demand=0)
        demand.save()
    
    if only_demand:
        Demand.update_calories(
            user_id=user_id, 
            protein=((0.2 * serializer.data['daily_calory_demand']) / 4),
            carbohydrates=((0.55 * serializer.data['daily_calory_demand']) / 4),
            fat=((0.25 * serializer.data['daily_calory_demand']) / 9)
        )
    else:
        Demand.update_calories(
            user_id=user_id,
            protein=serializer.data['protein'],
            fat=serializer.data['fat'],
            carbohydrates=serializer.data['carbohydrates']
        )

    actual_demand = Demand.objects.get(user_id=user_id, date=date.today())

    return Response({
            'daily_calory_demand' : actual_demand.daily_calory_demand,
            'protein' : actual_demand.protein,
            'carbohydrates' : actual_demand.carbohydrates,
            'fat' : actual_demand.fat,
        })



# MEAL VIEWS

@api_view(['GET'])
def api_detail_meal_view(request, meal_id):
    try:
        meal = Meal.objects.get(meal_id=meal_id)
    except Meal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = MealSerializer(meal)
    return Response(serializer.data) 

@api_view(['PUT'])
def api_update_meal_view(request, meal_id):
    try:
        meal = Meal.objects.get(meal_id=meal_id)
    except Meal.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = MealSerializer(meal, request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success' : 'update successful'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def api_delete_meal_view(request, meal_id):
    try:
        meal = Meal.objects.get(meal_id=meal_id)
    except Meal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    operation = Meal.objects.get(meal_id=meal_id).delete()
    data = {}
    if operation:
        data['success'] = 'deletion successful'
    else:
        data['failure'] = 'deletion failed'
    return Response(data)

@api_view(['POST'])
def api_create_meal_view(request):

    #user_id = request.user_id
    user_id = 1

    meal = Meal()

    serializer = MealSerializer(meal, request.data)
    if serializer.is_valid():
        Meal.add_meal(user_id=1, type=serializer.validated_data['type'], date=serializer.validated_data['date'])
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# MEAL ITEM VIEWS

@api_view(['GET'])
def api_detail_meal_item_view(request, meal_item_id):
    try:
        meal_item = MealItem.objects.get(id=meal_item_id)
    except MealItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MealItemSerializer(meal_item)
    return Response(serializer.data)

@api_view(['PUT'])
def api_update_meal_item_view(request, meal_item_id):
    try:
        meal_item = MealItem.objects.get(id=meal_item_id)
    except MealItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = MealItemSerializer(meal_item, request.data)
    data = {}
    if serializer.is_valid():
        data['success'] = 'update successful'
        serializer.save()
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def api_delete_meal_item_view(request, meal_item_id):
    try:
        meal_item = MealItem.objects.get(id=meal_item_id)
    except MealItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    operation = MealItem.objects.get(id=meal_item_id).delete()
    data = {}
    if operation:
        data['success'] = 'deletion successful'
    else:
        data['failure'] = 'deletion failed'
    return Response(data=data)

@api_view(['POST'])
def api_create_meal_item_view(request):
    meal_item = MealItem()
    serializer = MealItemSerializer(meal_item, request.data)

    if serializer.is_valid():
        MealItem.add_product(serializer.validated_data['meal_id'], serializer.validated_data['product_id'], serializer.validated_data['gram_amount'])
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)