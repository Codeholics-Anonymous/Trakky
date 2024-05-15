from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from utils.responses import custom_response, not_found_response
from rest_framework.decorators import api_view

from products_and_meals.models import (Product, Summary, Demand, Meal, MealItem)
from products_and_meals.api.serializers import (ProductSerializer, SummarySerializer, DemandSerializer, MealSerializer, MealItemSerializer)
from datetime import datetime, date

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q # to make more complex queries in db

# PRODUCT VIEWS

from utils.products_and_meals_utils import above_upper_limit

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_product_view(request, product_name):
    try:
        product = Product.objects.filter(Q(name__icontains=product_name) & (Q(user_id=1) | Q(user_id=request.user.id)))
        if (product is None):
            raise Product.DoesNotExist
    except Product.DoesNotExist:
        return not_found_response()

    serializer = ProductSerializer(product, many=True)
    for i in range(len(serializer.data)):
        serializer.data[i]['calories_per_hundred_grams'] = product[i].calories_per_hundred_grams
    return Response(serializer.data, status=status.HTTP_200_OK)

from utils.products_and_meals_utils import find_mealitems

@api_view(['PUT'])
def api_update_product_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return not_found_response()

    if (product.user_id != request.user.id): # user can edit only products that were created by him
        return custom_response("Product", "cannot be edited", status.HTTP_400_BAD_REQUEST)

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        # check if sum of macros isn't larger than 100g
        if above_upper_limit(serializer.validated_data['protein'], serializer.validated_data['carbohydrates'], serializer.validated_data['fat'], limit=100):
            return custom_response("Macros", f"amount to high ({serializer.validated_data['protein'] + serializer.validated_data['carbohydrates'] + serializer.validated_data['fat']}/{100})", status.HTTP_400_BAD_REQUEST) 
        # update today summary if this product was added (optimization - don't update past summaries)
        mealitems = find_mealitems(user_id=request.user.id, product_id=product_id, date=date.today()) # amount of products added today to summary
        mealitems_amount = len(mealitems)
        if (mealitems_amount != 0):
            # calculate product amount (grams)
            mealitems_gram_amount = 0
            for x in mealitems:
                mealitems_gram_amount += x.gram_amount
            # call function to calculate how many protein, carbohydrates and fat we have (using information about grams of product)
            all_product_macros = Product.calculate_nutrition(gram_amount=mealitems_gram_amount, product=product)
            # subtract calories, because past macros and calories of product aren't current
            Summary.update_calories( 
                user_id=request.user.id, 
                increase=0, 
                protein=all_product_macros[0], 
                carbohydrates=all_product_macros[1], 
                fat=all_product_macros[2], 
                date=date.today()
                )
        # update product information provided by user
        updated_product = Product.update_product(
            product_id=product_id, 
            name=serializer.validated_data['name'], 
            protein=serializer.validated_data['protein'],
            fat=serializer.validated_data['fat'],
            carbohydrates=serializer.validated_data['carbohydrates']
            )
        # after product update, we have to increase number of calories and macros in summary
        all_updated_product_macros = Product.calculate_nutrition(gram_amount=mealitems_gram_amount, product=updated_product)
        Summary.update_calories(
            user_id=request.user.id, 
            increase=1, 
            protein=all_updated_product_macros[0],
            carbohydrates=all_updated_product_macros[1],
            fat=all_updated_product_macros[2],
            date=date.today())
        return custom_response("Success", "update successful")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'],)
def api_delete_product_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return not_found_response()

    operation = product.delete()
    data = {}
    if operation:
        return custom_response("Success", "deletion successful")
    else:
        return custom_response("Failure", "deletion failed", status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_product_view(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        # check if this product exists in database
        if Product.objects.filter(name=serializer.validated_data['name']).exists():
            return Response({'Product' : 'already exist'})
        # check if sum of macros amount isn't larger than 100g
        if above_upper_limit(serializer.validated_data['protein'], serializer.validated_data['carbohydrates'], serializer.validated_data['fat'], limit=100):
            return custom_response("Macros", f"amount to high ({serializer.validated_data['protein'] + serializer.validated_data['carbohydrates'] + serializer.validated_data['fat']}/{100})", status.HTTP_400_BAD_REQUEST)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_detail_summary_view(request, starting_date, ending_date):
    summaries = Summary.objects.filter(user_id=request.user.id, date__range=(starting_date, ending_date))

    # empty summaries aren't store in database but we don't need to imitate they exist (anyway they will be included as 0)
    calories_sum = 0
    protein_sum = 0
    carbohydrates_sum = 0
    fat_sum = 0
    for x in summaries:
        calories_sum += x.daily_calory_intake
        protein_sum += x.protein
        carbohydrates_sum += x.carbohydrates
        fat_sum += x.fat

    return Response({'calories_sum' : round(calories_sum), 'protein_sum' : round(protein_sum, 1), 'carbohydrates_sum' : round(carbohydrates_sum, 1), 'fat_sum' : round(fat_sum, 1)})

# DEMAND VIEWS
# ways to create demand:
# 1 option - we are creating demand basing on data that user gave us during registration 
# 2 option - user can set his demand by himself (by giving us protein, carbohydrates, fat and calories) (this option is presented below)

from utils.products_and_meals_utils import find_basic_demand

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_demand_view(request, date, preference):
    # check if user want his personal demand or default demand created during registration
    if preference == 'personal':
        demand = Demand.objects.filter(user_id=request.user.id, date__lte=date).order_by('-date').first()
    elif preference == 'default':
        demand = find_basic_demand(request.user.id)

    if demand is None:
        return not_found_response()

    serializer = DemandSerializer(demand)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_demand_view(request):
    user_id = request.user.id
    serializer = DemandSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    EPSILON = 20 # absolute calorie error

    calories_sum = 4 * serializer.validated_data['protein'] + 4 * serializer.validated_data['carbohydrates'] + 9 * serializer.validated_data['fat']
    if (calories_sum > serializer.validated_data['daily_calory_demand'] + EPSILON):
        return Response({'Macros calories too high' : f'{calories_sum}'})
    elif (calories_sum < serializer.validated_data['daily_calory_demand'] - EPSILON):
        return Response({'Macros calories too low' : f'{calories_sum}'})

    try:
        # we cannot overwrite basic demand created during registration
        first_user_demand = find_basic_demand(user_id)
        found_demand = Demand.objects.filter(user_id=user_id, date=date.today()).order_by('-demand_id').first()
        if ((found_demand == first_user_demand) or (found_demand is None)): # first equation is because we don't want to overwrite basic demand
            raise Demand.DoesNotExist() 
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

# returns information about each meal from selected day with all mealitems included
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_detail_meal_view(request, date):
    try:
        meal = Meal.objects.filter(user_id=request.user.id, date=date)
    except Meal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # find mealitems added by user at this date

    query = Q()

    for x in meal:
        query = Q(meal_id=x.meal_id) | query

    mealitems = MealItem.objects.filter(query)

    # now get from this information all products info

    breakfast_meal_id = lunch_meal_id = dinner_meal_id = None

    for x in meal:
        if (x.type=='breakfast'):
            breakfast_meal_id = x.meal_id
        elif (x.type=='lunch'):
            lunch_meal_id = x.meal_id
        elif (x.type=='dinner'):
            dinner_meal_id = x.meal_id

    data = {
        'breakfast' : {},
        'lunch' : {},
        'dinner' : {}
    }

    i = j = k = 0 # iterators to add products named as product0, product1, ...

    for x in mealitems:
        product = Product.objects.get(product_id=x.product_id) # get product from database
        product_macros_info = Product.calculate_nutrition(gram_amount=x.gram_amount, product=product) # calculate macros per gram_amount
        product_info = {
            'mealitem_id' : x.meal_item_id,
            'product_id' : product.product_id,
            'name' : product.name,
            'protein' : round(product_macros_info[0], 1),
            'carbohydrates' : round(product_macros_info[1], 1),
            'fat' : round(product_macros_info[2], 1),
            'calories' : round(product_macros_info[0]*4+product_macros_info[1]*4+product_macros_info[2]*9),
            'grams' : x.gram_amount
        }
        if (breakfast_meal_id is not None) and (x.meal_id == breakfast_meal_id):
            data['breakfast'][f'product{i}'] = product_info
            i += 1
        elif (lunch_meal_id is not None) and (x.meal_id == lunch_meal_id):
            data['lunch'][f'product{j}'] = product_info
            j += 1
        if (dinner_meal_id is not None) and (x.meal_id == dinner_meal_id):
            data['dinner'][f'product{k}'] = product_info
            k += 1

    return Response(data, status=status.HTTP_200_OK) 

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

    
# MEALITEM VIEWS

@api_view(['GET'])
def api_detail_meal_item_view(request, meal_item_id):
    try:
        meal_item = MealItem.objects.get(meal_item_id=meal_item_id)
    except MealItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MealItemSerializer(meal_item)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_update_meal_item_view(request, meal_item_id):
    try:
        mealitem = MealItem.objects.get(meal_item_id=meal_item_id)
    except MealItem.DoesNotExist:
        return not_found_response()
    
    serializer = MealItemSerializer(mealitem, request.data)
    if serializer.is_valid():
        # get product 
        product = Product.objects.get(product_id=mealitem.product_id)
        grams_difference = serializer.validated_data['gram_amount'] - mealitem.gram_amount # calculate difference between grams
        product_macros = Product.calculate_nutrition(gram_amount=abs(grams_difference), product=product) # calculate calories per grams_difference
        print(grams_difference)
        # update summary
        meal_id = mealitem.meal_id # find id of meal this mealitem belongs to
        summary_date = Meal.objects.get(meal_id=meal_id).date # since we have mealitem, it must exist
        if grams_difference < 0:
            new_summary = Summary.update_calories(user_id=request.user.id, increase=0, protein=product_macros[0], carbohydrates=product_macros[1], fat=product_macros[2], date=summary_date)
        else:
            new_summary = Summary.update_calories(user_id=request.user.id, increase=1, protein=product_macros[0], carbohydrates=product_macros[1], fat=product_macros[2], date=summary_date)
        summary_serializer = SummarySerializer(new_summary)
        serializer.save()
        return Response(serializer.validated_data|summary_serializer.data, status=status.HTTP_200_OK)
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

def create_mealitem(type, user_id, request_data, date):
    # MEAL EXISTENCE
    if not Meal.objects.filter(user_id=user_id, date=date, type=type).exists():
        Meal.add_meal(user_id=user_id, type=type, date=date)
    # SUMMARY EXISTENCE
    if not Summary.objects.filter(user_id=user_id, date=date).exists():
        Summary.create_summary(user_id=user_id, date=date)
    # MEAL ITEM PART
    meal_id = Meal.objects.get(user_id=user_id, date=date, type=type).meal_id # now we can get meal_id because we know that meal exists
    serializer = MealItemSerializer(data=request_data)
    if serializer.is_valid():
        product_to_add = Product.objects.get(product_id=serializer.validated_data['product_id'])
        MealItem.add_product(meal_id=meal_id, product_id=product_to_add.product_id, gram_amount=serializer.validated_data['gram_amount'])
        # calculate product macros and calories (gram_amount of product can be different than 100)
        protein, carbohydrates, fat = Product.calculate_nutrition(gram_amount=serializer.validated_data['gram_amount'], product=product_to_add)
        # update summary
        Summary.update_calories(user_id=user_id, increase=True, protein=protein, carbohydrates=carbohydrates, fat=fat, date=date)
        # create data to return
        data = serializer.validated_data|{'name' : product_to_add.name, 'calories' : round((4*protein + 4*carbohydrates + 9*fat)), 'protein' : round(protein, 1), 'carbohydrates' : round(carbohydrates, 1), 'fat' : round(fat, 1)}
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_mealitem_breakfast_view(request, date):
    return create_mealitem(type="breakfast", user_id=request.user.id, request_data=request.data, date=date)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_mealitem_lunch_view(request, date):
    return create_mealitem(type="lunch", user_id=request.user.id, request_data=request.data, date=date)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_mealitem_dinner_view(request, date):
    return create_mealitem(type="dinner", user_id=request.user.id, request_data=request.data, date=date)
