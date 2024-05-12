from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from products_and_meals.models import (Product, Summary, Demand, Meal, MealItem)
from products_and_meals.api.serializers import (ProductSerializer, SummarySerializer, DemandSerializer, MealSerializer, MealItemSerializer)
from datetime import datetime, date

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q # to make more complex queries in db

# PRODUCT VIEWS

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_product_view(request, product_name):
    try:
        product = Product.objects.filter(Q(name__icontains=product_name) & (Q(user_id=1) | Q(user_id=request.user.id)))
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, many=True)
    for i in range(len(serializer.data)):
        serializer.data[i]['calories_per_hundred_grams'] = product[i].calories_per_hundred_grams
    return Response(serializer.data)

@api_view(['PUT'])
def api_update_product_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, data=request.data)
    data = {}
    if serializer.is_valid():
        Product.update_product(
            product_id, 
            new_name=serializer.validated_data['name'], 
            new_protein=serializer.validated_data['protein'],
            new_fat=serializer.validated_data['fat'],
            new_carbohydrates=serializer.validated_data['carbohydrates']
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
#TODO CHECK IF THIS OBJECT DOES NOT EXIST IN DATABASE - IF EXISTS, DON'T ADD DUPLICATE
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_product_view(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        # check if sum of macros amount isn't larger than 100g
        macros_amount = serializer.validated_data['protein'] + serializer.validated_data['carbohydrates'] + serializer.validated_data['fat']
        if macros_amount > 100:
            return Response({'Macros amount' : 'too high'})
        # add product
        added_product = Product.add_product(
            user_id=request.user.id,
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
# ways to create demand:
# 1 option - we are creating demand when basing on data that user gave us
# 2 option - user can set his demand by himself (by giving us protein, carbohydrates, fat and calories)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_demand_view(request, date):
    demand = Demand.objects.filter(user_id=request.user.id, date__lte=date).order_by('-date').first()
    if demand is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = DemandSerializer(demand)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_demand_view(request):
    user_id = request.user.id
    serializer = DemandSerializer(data=request.data)

    EPSILON = 10 # absolute calorie error

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    calories_sum = 4 * serializer.validated_data['protein'] + 4 * serializer.validated_data['carbohydrates'] + 9 * serializer.validated_data['fat']
    if (calories_sum > serializer.validated_data['daily_calory_demand'] + EPSILON):
        return Response({'Macros calories too high' : f'{calories_sum}'})
    elif (calories_sum < serializer.validated_data['daily_calory_demand'] - EPSILON):
        return Response({'Macros calories too low' : f'{calories_sum}'})

    try:
        Demand.objects.get(user_id=user_id, date=date.today()) 
        Demand.update_calories(
            user_id=user_id, 
            protein=serializer.validated_data['protein'],
            carbohydrates=serializer.validated_data['carbohydrates'],
            fat=serializer.validated_data['fat'],
            daily_calory_demand=serializer.validated_data['daily_calory_demand'])
    except Demand.DoesNotExist:
        Demand.create_demand(
            user_id=user_id,
            protein=serializer.validated_data['protein'],
            carbohydrates=serializer.validated_data['carbohydrates'],
            fat=serializer.validated_data['fat'],
            daily_calory_demand=serializer.validated_data['daily_calory_demand'],
            date=date.today()
            )

    return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

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