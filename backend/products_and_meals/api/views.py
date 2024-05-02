from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from products_and_meals.models import (Product, Summary, Demand, Meal, MealItem)
from products_and_meals.api.serializers import (ProductSerializer, SummarySerializer, DemandSerializer, MealSerializer, MealItemSerializer)

# PRODUCT VIEWS

@api_view(['GET'])
def api_detail_product_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
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

    if request.method == 'POST':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            if ('calories_per_hundred_grams' not in serializer.validated_data):
                serializer.validated_data['calories_per_hundred_grams'] = None
            Product.add_product(
                serializer.validated_data['name'],
                serializer.validated_data['calories_per_hundred_grams'],
                serializer.validated_data['protein'],
                serializer.validated_data['carbohydrates'],
                serializer.validated_data['fat'],
            )
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
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
    try:
        demand = Demand.objects.filter(user_id=user_id, date__lte=date).order_by('-date').first()
    except Demand.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DemandSerializer(demand)
        return Response(serializer.data)        

@api_view(['POST'])
def api_create_demand_view(request):
    #user_id = request.user.id
    user_id = 1

    demand = Demand(user_id=user_id)
    serializer = DemandSerializer(demand, request.data)
    if serializer.is_valid():
        Demand.create_demand(
            user_id,
            serializer.validated_data['date'],
            serializer.validated_data['protein'],
            serializer.validated_data['carbohydrates'],
            serializer.validated_data['fat']
        )
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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